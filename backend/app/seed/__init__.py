"""Repeatable seed for the curriculum.

Records are matched by stable keys (course slug, CEFR level, unit slug, lesson slug,
learning-item key, exercise key), so rerunning never creates duplicates.

- Default mode creates missing records and leaves existing ones untouched, so content
  edited later in the CMS is not overwritten.
- `update=True` re-applies the seed content. Changed exercises get a new `version`;
  changed lessons get a new `content_version`, so old attempts stay interpretable.

The seed never creates user accounts (use `python -m app.cli create-admin`).
"""

from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exercises.definitions import validate_definition
from app.models import (
    Course,
    CourseLevel,
    Exercise,
    ExerciseAttempt,
    ExerciseLearningItem,
    LearningItem,
    Lesson,
    LessonLearningItem,
    StoryEpisode,
    Unit,
)
from app.models.enums import (
    CefrLevel,
    ExerciseType,
    LearningItemKind,
    LessonItemRole,
    LessonSection,
    PublicationStatus,
    RecallMode,
)
from app.schemas.content import LessonContent
from app.seed import little_explorers as data

PUB = PublicationStatus.PUBLISHED


@dataclass
class SeedReport:
    created: dict[str, int] = field(default_factory=dict)
    updated: dict[str, int] = field(default_factory=dict)

    def add(self, bucket: dict[str, int], kind: str) -> None:
        bucket[kind] = bucket.get(kind, 0) + 1

    def summary(self) -> str:
        def fmt(d: dict[str, int]) -> str:
            return ", ".join(f"{v} {k}" for k, v in sorted(d.items())) or "nothing"

        return f"created: {fmt(self.created)}; updated: {fmt(self.updated)}"


def validate_seed_data() -> None:
    """Fail fast if any seed lesson/exercise is invalid or references unknown items."""
    for lesson in data.LESSONS:
        LessonContent.model_validate(lesson["content"])
        keys = [e["key"] for e in lesson["exercises"]]
        if len(keys) != len(set(keys)):
            raise ValueError(f"Duplicate exercise key in {lesson['slug']}")
        for ex in lesson["exercises"]:
            validate_definition(ExerciseType(ex["type"]), ex["prompt"], ex["answer"])
            for key in ex["items"]:
                if key not in data.ITEMS:
                    raise ValueError(f"Unknown learning item {key} in {lesson['slug']}/{ex['key']}")
        for key in lesson["review"]:
            if key not in data.ITEMS:
                raise ValueError(f"Unknown review item {key} in {lesson['slug']}")


def _set(obj: object, values: dict, report: SeedReport, kind: str, update: bool) -> bool:
    """Apply values when updating; return True if anything changed."""
    if not update:
        return False
    changed = {k: v for k, v in values.items() if getattr(obj, k) != v}
    for k, v in changed.items():
        setattr(obj, k, v)
    if changed:
        report.add(report.updated, kind)
    return bool(changed)


def run_seed(db: Session, update: bool = False) -> SeedReport:
    validate_seed_data()
    report = SeedReport()

    # Course / level / unit -------------------------------------------------------------
    course = db.scalar(select(Course).where(Course.slug == data.COURSE["slug"]))
    if course is None:
        course = Course(
            slug=data.COURSE["slug"],
            title=data.COURSE["title"],
            description=data.COURSE["description"],
            status=PUB,
        )
        db.add(course)
        report.add(report.created, "courses")
        update_course = False
    else:
        update_course = update
    _set(
        course,
        {"title": data.COURSE["title"], "description": data.COURSE["description"]},
        report,
        "courses",
        update_course,
    )

    db.flush()
    level = db.scalar(
        select(CourseLevel).where(
            CourseLevel.course_id == course.id, CourseLevel.cefr_level == CefrLevel.A1
        )
    )
    if level is None:
        level = CourseLevel(
            course_id=course.id,
            cefr_level=CefrLevel.A1,
            title=data.LEVEL["title"],
            description=data.LEVEL["description"],
            position=1,
        )
        db.add(level)
        report.add(report.created, "levels")
        update_level = False
    else:
        update_level = update
    _set(
        level,
        {"title": data.LEVEL["title"], "description": data.LEVEL["description"]},
        report,
        "levels",
        update_level,
    )

    db.flush()
    unit = db.scalar(select(Unit).where(Unit.level_id == level.id, Unit.slug == data.UNIT["slug"]))
    if unit is None:
        unit = Unit(
            level_id=level.id,
            slug=data.UNIT["slug"],
            title=data.UNIT["title"],
            description=data.UNIT["description"],
            position=1,
        )
        db.add(unit)
        report.add(report.created, "units")
        update_unit = False
    else:
        update_unit = update
    _set(
        unit,
        {"title": data.UNIT["title"], "description": data.UNIT["description"]},
        report,
        "units",
        update_unit,
    )
    db.flush()

    # Lessons (needed before items, which reference their introducing lesson) ------------
    lessons: dict[int, Lesson] = {}
    lesson_is_new: dict[int, bool] = {}
    for number, spec in enumerate(data.LESSONS, start=1):
        lesson = db.scalar(
            select(Lesson).where(Lesson.unit_id == unit.id, Lesson.slug == spec["slug"])
        )
        content = LessonContent.model_validate(spec["content"]).model_dump(
            mode="json", exclude_none=True
        )
        values = {
            "title": spec["title"],
            "description": spec["description"],
            "objectives": spec["objectives"],
            "cefr_level": CefrLevel.A1,
            "position": number,
            "estimated_minutes": spec["minutes"],
            "content": content,
        }
        if lesson is None:
            lesson = Lesson(
                unit_id=unit.id, slug=spec["slug"], status=PUB, content_version=1, **values
            )
            db.add(lesson)
            report.add(report.created, "lessons")
            lesson_is_new[number] = True
        else:
            lesson_is_new[number] = False
            if _set(lesson, values, report, "lessons", update):
                lesson.content_version += 1
        lessons[number] = lesson
    db.flush()

    # Learning items ----------------------------------------------------------------------
    items: dict[str, LearningItem] = {}
    item_lesson: dict[str, int] = {}
    for key, (kind, text, emoji, ru, lesson_no, examples, explanation) in data.ITEMS.items():
        item_lesson[key] = lesson_no
        values = {
            "kind": LearningItemKind(kind),
            "text": text,
            "emoji": emoji,
            "translation_ru": ru,
            "cefr_level": CefrLevel.A1,
            "examples": examples,
            "explanation": explanation,
            "introduced_in_lesson_id": lessons[lesson_no].id,
        }
        item = db.scalar(select(LearningItem).where(LearningItem.key == key))
        if item is None:
            item = LearningItem(key=key, **values)
            db.add(item)
            report.add(report.created, "learning_items")
        else:
            _set(item, values, report, "learning_items", update)
        items[key] = item
    db.flush()

    # Exercises, item links, lesson item roles, episodes --------------------------------
    for number, spec in enumerate(data.LESSONS, start=1):
        lesson = lessons[number]
        if not lesson_is_new[number] and not update:
            continue
        used_items: set[str] = set(spec["review"])
        for position, ex in enumerate(spec["exercises"], start=1):
            used_items |= set(ex["items"])
            _upsert_exercise(db, lesson, ex, position, items, report, update)
        _remove_stale_exercises(db, lesson, {e["key"] for e in spec["exercises"]}, report)
        _sync_lesson_items(db, lesson, number, used_items, items, item_lesson)
        _upsert_episode(db, lesson, spec["episode"], report, update)

    db.commit()
    return report


def _upsert_exercise(db, lesson, ex, position, items, report, update) -> None:
    ex_type = ExerciseType(ex["type"])
    prompt, answer = validate_definition(ex_type, ex["prompt"], ex["answer"])
    values = {
        "type": ex_type,
        "section": LessonSection(ex["section"]),
        "recall_mode": RecallMode(ex["mode"]),
        "position": position,
        "instructions": ex["instructions"],
        "prompt": prompt,
        "answer": answer,
        "feedback": ex["feedback"],
        "points": ex["points"],
        "is_scored": ex_type != ExerciseType.SPEAKING,
    }
    exercise = db.scalar(
        select(Exercise).where(Exercise.lesson_id == lesson.id, Exercise.key == ex["key"])
    )
    if exercise is None:
        exercise = Exercise(lesson_id=lesson.id, key=ex["key"], version=1, **values)
        db.add(exercise)
        db.flush()
        report.add(report.created, "exercises")
    else:
        before = (exercise.type, exercise.prompt, exercise.answer, exercise.points)
        if _set(exercise, values, report, "exercises", update) and before != (
            exercise.type,
            exercise.prompt,
            exercise.answer,
            exercise.points,
        ):
            exercise.version += 1
    wanted = {items[k].id for k in ex["items"]}
    current = {link.learning_item_id: link for link in exercise.item_links}
    for item_id, link in current.items():
        if item_id not in wanted:
            db.delete(link)
    for item_id in wanted - set(current):
        db.add(ExerciseLearningItem(exercise_id=exercise.id, learning_item_id=item_id))


def _remove_stale_exercises(db, lesson, keys: set[str], report) -> None:
    """Exercises no longer in the seed are deleted only if nobody has attempted them."""
    for exercise in list(lesson.exercises):
        if exercise.key in keys:
            continue
        has_attempts = db.scalar(
            select(ExerciseAttempt.id).where(ExerciseAttempt.exercise_id == exercise.id).limit(1)
        )
        if not has_attempts:
            db.delete(exercise)
            report.add(report.updated, "exercises_removed")


def _sync_lesson_items(db, lesson, number, used, items, item_lesson) -> None:
    """NEW = introduced here; RECENT_REVIEW = previous lesson; OLDER_REVIEW = earlier."""
    wanted: dict = {}
    for key in used:
        introduced = item_lesson[key]
        if introduced > number:
            raise ValueError(f"{key} is used in lesson {number} before it is introduced")
        if introduced == number:
            role = LessonItemRole.NEW
        elif introduced == number - 1:
            role = LessonItemRole.RECENT_REVIEW
        else:
            role = LessonItemRole.OLDER_REVIEW
        wanted[items[key].id] = role
    # Every item introduced in this lesson is NEW even if no exercise practises it yet.
    for key, introduced in item_lesson.items():
        if introduced == number:
            wanted[items[key].id] = LessonItemRole.NEW
    existing = {
        link.learning_item_id: link
        for link in db.scalars(
            select(LessonLearningItem).where(LessonLearningItem.lesson_id == lesson.id)
        )
    }
    for item_id, link in existing.items():
        if item_id not in wanted:
            db.delete(link)
        elif link.role != wanted[item_id]:
            link.role = wanted[item_id]
    for item_id, role in wanted.items():
        if item_id not in existing:
            db.add(LessonLearningItem(lesson_id=lesson.id, learning_item_id=item_id, role=role))


def _upsert_episode(db, lesson, episode_spec, report, update) -> None:
    title, synopsis = episode_spec
    episode = db.scalar(
        select(StoryEpisode).where(StoryEpisode.lesson_id == lesson.id, StoryEpisode.position == 1)
    )
    if episode is None:
        # Published without video: the lesson shows "video coming soon" until one is attached.
        db.add(
            StoryEpisode(
                lesson_id=lesson.id, title=title, synopsis=synopsis, position=1, status=PUB
            )
        )
        report.add(report.created, "episodes")
    else:
        _set(episode, {"title": title, "synopsis": synopsis}, report, "episodes", update)
