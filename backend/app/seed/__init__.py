"""Repeatable seed for the curriculum.

Records are matched by stable keys (course slug, CEFR level, unit slug, lesson slug,
learning-item key, exercise key), so rerunning never creates duplicates.

- Default mode creates missing records and leaves existing ones untouched, so content
  edited later in the CMS is not overwritten.
- `update=True` re-applies the seed content. Changed exercises get a new `version`;
  changed lessons get a new `content_version`, so old attempts stay interpretable.
- Character names ({boy}, {little}, ...) are filled in from app/seed/characters.py.

The seed never creates user accounts (use `python -m app.cli create-admin`).
"""

from dataclasses import dataclass, field
from typing import Any

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
from app.seed import content as raw_content
from app.seed.characters import load_names, personalize

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


@dataclass
class SeedData:
    course: dict[str, Any]
    levels: list[dict[str, Any]]
    items: dict[str, tuple]

    def lessons(self) -> list[tuple[dict, dict, dict]]:
        """(level, unit, lesson) in course order."""
        return [
            (level, unit, lesson)
            for level in self.levels
            for unit in level["units"]
            for lesson in unit["lessons"]
        ]


def load_seed_data(names: dict[str, str] | None = None) -> SeedData:
    names = names or load_names()
    return SeedData(
        course=personalize(raw_content.COURSE, names),
        levels=personalize(raw_content.LEVELS, names),
        items=personalize(raw_content.ITEMS, names),
    )


def validate_seed_data(data: SeedData) -> None:
    """Fail fast on invalid content, unknown items, or items used before introduced."""
    order = {lesson["slug"]: i for i, (_, _, lesson) in enumerate(data.lessons())}
    if len(order) != len(data.lessons()):
        raise ValueError("Lesson slugs must be unique across the course.")
    for key, item in data.items.items():
        if item[4] not in order:
            raise ValueError(f"Item {key} is introduced in unknown lesson {item[4]}")
    for _, _, lesson in data.lessons():
        LessonContent.model_validate(lesson["content"])
        keys = [e["key"] for e in lesson["exercises"]]
        if len(keys) != len(set(keys)):
            raise ValueError(f"Duplicate exercise key in {lesson['slug']}")
        used = set(lesson["review"])
        for ex in lesson["exercises"]:
            validate_definition(ExerciseType(ex["type"]), ex["prompt"], ex["answer"])
            used |= set(ex["items"])
        for key in used:
            if key not in data.items:
                raise ValueError(f"Unknown learning item {key} in {lesson['slug']}")
            if order[data.items[key][4]] > order[lesson["slug"]]:
                raise ValueError(f"{key} is used in {lesson['slug']} before it is introduced")


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


def run_seed(db: Session, update: bool = False, data: SeedData | None = None) -> SeedReport:
    data = data or load_seed_data()
    validate_seed_data(data)
    report = SeedReport()

    course_values = {"title": data.course["title"], "description": data.course["description"]}
    course = db.scalar(select(Course).where(Course.slug == data.course["slug"]))
    if course is None:
        course = Course(slug=data.course["slug"], status=PUB, **course_values)
        db.add(course)
        db.flush()
        report.add(report.created, "courses")
    else:
        _set(course, course_values, report, "courses", update)

    # Structure + lessons ------------------------------------------------------------------
    lessons: dict[str, Lesson] = {}
    new_lessons: set[str] = set()
    for level_pos, level_spec in enumerate(data.levels, start=1):
        cefr = CefrLevel(level_spec["cefr"])
        level_values = {
            "title": level_spec["title"],
            "description": level_spec["description"],
            "position": level_pos,
        }
        level = db.scalar(
            select(CourseLevel).where(
                CourseLevel.course_id == course.id, CourseLevel.cefr_level == cefr
            )
        )
        if level is None:
            level = CourseLevel(course_id=course.id, cefr_level=cefr, **level_values)
            db.add(level)
            db.flush()
            report.add(report.created, "levels")
        else:
            _set(level, level_values, report, "levels", update)

        for unit_pos, unit_spec in enumerate(level_spec["units"], start=1):
            unit_values = {
                "title": unit_spec["title"],
                "description": unit_spec["description"],
                "position": unit_pos,
            }
            unit = db.scalar(
                select(Unit).where(Unit.level_id == level.id, Unit.slug == unit_spec["slug"])
            )
            if unit is None:
                unit = Unit(level_id=level.id, slug=unit_spec["slug"], **unit_values)
                db.add(unit)
                db.flush()
                report.add(report.created, "units")
            else:
                _set(unit, unit_values, report, "units", update)

            for lesson_pos, spec in enumerate(unit_spec["lessons"], start=1):
                lesson, created = _upsert_lesson(db, unit, cefr, lesson_pos, spec, report, update)
                if created:
                    new_lessons.add(spec["slug"])
                lessons[spec["slug"]] = lesson
    db.flush()

    # Learning items ------------------------------------------------------------------------
    items: dict[str, LearningItem] = {}
    for key, (kind, text, emoji, ru, lesson_slug, examples, explanation) in data.items.items():
        lesson = lessons[lesson_slug]
        values = {
            "kind": LearningItemKind(kind),
            "text": text,
            "emoji": emoji,
            "translation_ru": ru,
            "cefr_level": lesson.cefr_level,
            "examples": examples,
            "explanation": explanation,
            "introduced_in_lesson_id": lesson.id,
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

    # Exercises, links, review roles, episodes ----------------------------------------------
    position_of = {lesson["slug"]: i for i, (_, _, lesson) in enumerate(data.lessons())}
    item_lesson = {key: position_of[item[4]] for key, item in data.items.items()}
    for _, _, spec in data.lessons():
        lesson = lessons[spec["slug"]]
        if spec["slug"] not in new_lessons and not update:
            continue
        used: set[str] = set(spec["review"])
        for position, ex in enumerate(spec["exercises"], start=1):
            used |= set(ex["items"])
            _upsert_exercise(db, lesson, ex, position, items, report, update)
        _remove_stale_exercises(db, lesson, {e["key"] for e in spec["exercises"]}, report)
        _sync_lesson_items(db, lesson, position_of[spec["slug"]], used, items, item_lesson)
        _upsert_episode(db, lesson, spec["episode"], report, update)

    db.commit()
    return report


def _upsert_lesson(db, unit, cefr, position, spec, report, update) -> tuple[Lesson, bool]:
    content = LessonContent.model_validate(spec["content"]).model_dump(
        mode="json", exclude_none=True
    )
    values = {
        "title": spec["title"],
        "description": spec["description"],
        "objectives": spec["objectives"],
        "cefr_level": cefr,
        "position": position,
        "estimated_minutes": spec["minutes"],
        "content": content,
    }
    lesson = db.scalar(select(Lesson).where(Lesson.unit_id == unit.id, Lesson.slug == spec["slug"]))
    if lesson is None:
        lesson = Lesson(unit_id=unit.id, slug=spec["slug"], status=PUB, content_version=1, **values)
        db.add(lesson)
        db.flush()
        report.add(report.created, "lessons")
        return lesson, True
    if _set(lesson, values, report, "lessons", update):
        lesson.content_version += 1
    return lesson, False


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


def _sync_lesson_items(db, lesson, index, used, items, item_lesson) -> None:
    """NEW = introduced here; RECENT_REVIEW = previous lesson; OLDER_REVIEW = earlier."""
    wanted: dict = {}
    for key in used:
        introduced = item_lesson[key]
        if introduced == index:
            role = LessonItemRole.NEW
        elif introduced == index - 1:
            role = LessonItemRole.RECENT_REVIEW
        else:
            role = LessonItemRole.OLDER_REVIEW
        wanted[items[key].id] = role
    # Every item introduced in this lesson is NEW even if no exercise practises it yet.
    for key, introduced in item_lesson.items():
        if introduced == index:
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
