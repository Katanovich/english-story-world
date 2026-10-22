"""Builds a small published course for tests (real content comes from the seed in Part 4)."""

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.exercises.definitions import validate_definition
from app.models import (
    Course,
    CourseLevel,
    Enrollment,
    Exercise,
    ExerciseLearningItem,
    LearningItem,
    Lesson,
    LessonLearningItem,
    StoryEpisode,
    Unit,
    User,
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

PUB = PublicationStatus.PUBLISHED


@dataclass
class World:
    course: Course
    lessons: list[Lesson]
    draft: Lesson
    items: dict[str, LearningItem]
    ex: dict[str, Exercise] = field(default_factory=dict)
    episode: StoryEpisode | None = None


def _exercise(
    db,
    lesson,
    key,
    ex_type,
    section,
    prompt,
    answer,
    items,
    mode=RecallMode.RECOGNITION,
    points=1,
    position=0,
    feedback=None,
):
    prompt, answer = validate_definition(ex_type, prompt, answer)
    e = Exercise(
        lesson=lesson,
        key=key,
        type=ex_type,
        section=section,
        recall_mode=mode,
        position=position,
        instructions=f"Do {key}",
        prompt=prompt,
        answer=answer,
        feedback=feedback
        or {
            "correct": "Yes!",
            "incorrect": "Try again.",
            "hint": "Look closely.",
            "explanation": "Because.",
        },
        points=points,
        is_scored=ex_type != ExerciseType.SPEAKING,
    )
    db.add(e)
    db.flush()
    for item in items:
        db.add(ExerciseLearningItem(exercise_id=e.id, learning_item_id=item.id))
    return e


def build_world(db: Session) -> World:
    course = Course(slug="test-course", title="Test Course", status=PUB)
    level = CourseLevel(course=course, cefr_level=CefrLevel.A1, title="A1", position=1)
    unit = Unit(level=level, slug="u1", title="Unit 1", position=1)
    l1 = Lesson(
        unit=unit,
        slug="l1",
        title="Lesson 1",
        cefr_level=CefrLevel.A1,
        position=1,
        status=PUB,
        objectives=["Say hello"],
        content={"reading": {"title": "Hi", "paragraphs": [{"sentences": ["Hello!"]}]}},
    )
    l2 = Lesson(
        unit=unit, slug="l2", title="Lesson 2", cefr_level=CefrLevel.A1, position=2, status=PUB
    )
    draft = Lesson(unit=unit, slug="l3", title="Draft", cefr_level=CefrLevel.A1, position=3)
    db.add_all([course, level, unit, l1, l2, draft])
    db.flush()

    items = {
        k: LearningItem(
            key=f"vocab.{k}",
            kind=LearningItemKind.VOCABULARY,
            text=k,
            cefr_level=CefrLevel.A1,
            introduced_in_lesson_id=l1.id,
        )
        for k in ("mother", "father")
    }
    db.add_all(items.values())
    db.flush()
    for it in items.values():
        db.add(LessonLearningItem(lesson_id=l1.id, learning_item_id=it.id, role=LessonItemRole.NEW))
        db.add(
            LessonLearningItem(
                lesson_id=l2.id, learning_item_id=it.id, role=LessonItemRole.RECENT_REVIEW
            )
        )

    w = World(course=course, lessons=[l1, l2], draft=draft, items=items)
    w.ex["choice"] = _exercise(
        db,
        l1,
        "choice",
        ExerciseType.MULTIPLE_CHOICE,
        LessonSection.VOCABULARY,
        {
            "question": "Who is this?",
            "options": [{"id": "a", "text": "mother"}, {"id": "b", "text": "father"}],
        },
        {"correct": "a"},
        [items["mother"]],
        position=1,
    )
    w.ex["build"] = _exercise(
        db,
        l1,
        "build",
        ExerciseType.SENTENCE_BUILDER,
        LessonSection.GRAMMAR,
        {"tiles": ["This", "is", "my", "mother"]},
        {"accepted": ["This is my mother."]},
        [items["mother"]],
        mode=RecallMode.RECALL,
        points=2,
        position=2,
    )
    w.ex["quiz"] = _exercise(
        db,
        l1,
        "quiz",
        ExerciseType.FILL_BLANK,
        LessonSection.QUIZ,
        {"text": "My ___ is Tom.", "word_bank": ["father", "table"]},
        {"blanks": [["father"]]},
        [items["father"]],
        mode=RecallMode.RECALL,
        position=3,
    )
    w.ex["speak"] = _exercise(
        db,
        l1,
        "speak",
        ExerciseType.SPEAKING,
        LessonSection.SPEAKING,
        {"text": "Say: This is my mother.", "model_answer": "This is my mother."},
        {},
        [],
        position=4,
    )
    w.ex["l2"] = _exercise(
        db,
        l2,
        "tf",
        ExerciseType.TRUE_FALSE,
        LessonSection.QUIZ,
        {"statement": "A mother is a woman."},
        {"correct": True},
        [items["mother"]],
    )
    w.episode = StoryEpisode(
        lesson_id=l1.id, title="Meet the family", synopsis="Alex says hi.", position=1, status=PUB
    )
    db.add(w.episode)
    db.commit()
    return w


def enroll(db: Session, user: User, course: Course) -> Enrollment:
    e = Enrollment(user_id=user.id, course_id=course.id)
    db.add(e)
    db.commit()
    return e
