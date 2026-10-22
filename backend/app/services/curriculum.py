"""Curriculum access rules and learner-facing serialisation."""

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.errors import AppError
from app.exercises.definitions import public_prompt
from app.models import (
    Course,
    CourseLevel,
    Enrollment,
    Exercise,
    ExerciseAttempt,
    LearningItem,
    Lesson,
    LessonLearningItem,
    LessonProgress,
    MediaAsset,
    Unit,
    User,
)
from app.models.enums import (
    EnrollmentStatus,
    LessonProgressStatus,
    PublicationStatus,
    UserRole,
)
from app.schemas.curriculum import (
    CourseTree,
    EpisodeOut,
    ExercisePublic,
    LearningItemOut,
    LessonDetail,
    LessonItemOut,
    LessonProgressOut,
    LessonSummary,
    LevelOut,
    MediaRef,
    UnitOut,
)

PUBLISHED = PublicationStatus.PUBLISHED


def course_of_lesson(db: Session, lesson: Lesson) -> Course:
    return db.scalars(
        select(Course)
        .join(CourseLevel, CourseLevel.course_id == Course.id)
        .join(Unit, Unit.level_id == CourseLevel.id)
        .where(Unit.id == lesson.unit_id)
    ).one()


def active_enrollment(db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> Enrollment | None:
    return db.scalar(
        select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
        )
    )


def get_accessible_lesson(db: Session, user: User, lesson_id: uuid.UUID) -> tuple[Lesson, Course]:
    """Students: published lesson in a published course they are enrolled in.
    Admins: any lesson (used for preview). Everything else is a 404, so lesson ids of
    other courses cannot be probed."""
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise AppError(404, "Lesson not found.")
    course = course_of_lesson(db, lesson)
    if user.role == UserRole.ADMIN:
        return lesson, course
    if (
        lesson.status != PUBLISHED
        or course.status != PUBLISHED
        or active_enrollment(db, user.id, course.id) is None
    ):
        raise AppError(404, "Lesson not found.")
    return lesson, course


def ordered_lessons(db: Session, course_id: uuid.UUID, published_only: bool) -> list[Lesson]:
    stmt = (
        select(Lesson)
        .join(Unit, Unit.id == Lesson.unit_id)
        .join(CourseLevel, CourseLevel.id == Unit.level_id)
        .where(CourseLevel.course_id == course_id)
        .order_by(CourseLevel.position, Unit.position, Lesson.position)
    )
    if published_only:
        stmt = stmt.where(Lesson.status == PUBLISHED)
    return list(db.scalars(stmt))


def progress_map(db: Session, user_id: uuid.UUID) -> dict[uuid.UUID, LessonProgress]:
    rows = db.scalars(select(LessonProgress).where(LessonProgress.user_id == user_id))
    return {p.lesson_id: p for p in rows}


def lesson_summary(lesson: Lesson, progress: LessonProgress | None) -> LessonSummary:
    return LessonSummary(
        id=lesson.id,
        slug=lesson.slug,
        title=lesson.title,
        description=lesson.description,
        position=lesson.position,
        estimated_minutes=lesson.estimated_minutes,
        cefr_level=lesson.cefr_level,
        cover_image_id=lesson.cover_image_id,
        progress_status=progress.status if progress else LessonProgressStatus.NOT_STARTED,
    )


def course_tree(
    db: Session, course: Course, user: User, enrollment: Enrollment | None
) -> CourseTree:
    published_only = user.role != UserRole.ADMIN
    progress = progress_map(db, user.id)
    course = db.scalars(
        select(Course)
        .where(Course.id == course.id)
        .options(
            selectinload(Course.levels).selectinload(CourseLevel.units).selectinload(Unit.lessons)
        )
    ).one()
    levels = []
    for level in course.levels:
        units = []
        for unit in level.units:
            lessons = [
                lesson_summary(lesson, progress.get(lesson.id))
                for lesson in unit.lessons
                if not published_only or lesson.status == PUBLISHED
            ]
            if lessons or not published_only:
                units.append(
                    UnitOut(
                        id=unit.id, title=unit.title, description=unit.description, lessons=lessons
                    )
                )
        if units or not published_only:
            levels.append(
                LevelOut(id=level.id, cefr_level=level.cefr_level, title=level.title, units=units)
            )
    return CourseTree(
        id=course.id,
        slug=course.slug,
        title=course.title,
        description=course.description,
        current_level=enrollment.current_level if enrollment else None,
        current_lesson_id=enrollment.current_lesson_id if enrollment else None,
        levels=levels,
    )


def progress_out(db: Session, progress: LessonProgress | None) -> LessonProgressOut | None:
    if progress is None:
        return None
    attempted = db.scalars(
        select(ExerciseAttempt.exercise_id)
        .where(
            ExerciseAttempt.user_id == progress.user_id,
            ExerciseAttempt.lesson_id == progress.lesson_id,
        )
        .distinct()
    ).all()
    out = LessonProgressOut.model_validate(progress)
    out.attempted_exercise_ids = list(attempted)
    return out


def exercise_public(exercise: Exercise) -> ExercisePublic:
    out = ExercisePublic.model_validate(exercise)
    out.prompt = public_prompt(exercise.type, exercise.prompt)
    return out


def _collect_media_ids(value: Any, found: set[uuid.UUID]) -> None:
    """Find every *_id field holding a media UUID inside nested JSON."""
    if isinstance(value, dict):
        for k, v in value.items():
            if k in ("image_id", "audio_id", "subtitle_id", "model_audio_id") and v:
                try:
                    found.add(uuid.UUID(str(v)))
                except ValueError:
                    pass
            else:
                _collect_media_ids(v, found)
    elif isinstance(value, list):
        for v in value:
            _collect_media_ids(v, found)


def media_refs(db: Session, ids: set[uuid.UUID]) -> dict[str, MediaRef]:
    if not ids:
        return {}
    assets = db.scalars(select(MediaAsset).where(MediaAsset.id.in_(ids)))
    return {str(a.id): MediaRef.model_validate(a) for a in assets}


def lesson_detail(db: Session, user: User, lesson: Lesson, course: Course) -> LessonDetail:
    is_admin = user.role == UserRole.ADMIN
    item_rows = db.execute(
        select(LessonLearningItem.role, LearningItem)
        .join(LearningItem, LearningItem.id == LessonLearningItem.learning_item_id)
        .where(LessonLearningItem.lesson_id == lesson.id)
        .order_by(LessonLearningItem.role, LearningItem.text)
    ).all()
    items = [
        LessonItemOut(role=role, item=LearningItemOut.model_validate(i)) for role, i in item_rows
    ]
    exercises = [exercise_public(e) for e in lesson.exercises]
    episodes = [
        EpisodeOut(
            id=ep.id,
            title=ep.title,
            synopsis=ep.synopsis,
            position=ep.position,
            video_asset_id=ep.video_asset_id,
            subtitle_asset_id=ep.subtitle_asset_id,
            poster_image_id=ep.poster_image_id,
            has_video=ep.video_asset_id is not None,
        )
        for ep in lesson.episodes
        if is_admin or ep.status == PUBLISHED
    ]

    ids: set[uuid.UUID] = set()
    _collect_media_ids(lesson.content, ids)
    for e in exercises:
        _collect_media_ids(e.prompt, ids)
        ids |= {i for i in (e.image_id, e.audio_id) if i}
    for li in items:
        ids |= {i for i in (li.item.image_id, li.item.audio_id) if i}
    for ep in episodes:
        ids |= {i for i in (ep.video_asset_id, ep.subtitle_asset_id, ep.poster_image_id) if i}
    if lesson.cover_image_id:
        ids.add(lesson.cover_image_id)

    sequence = ordered_lessons(db, course.id, published_only=not is_admin)
    ids_in_order = [lsn.id for lsn in sequence]
    idx = ids_in_order.index(lesson.id) if lesson.id in ids_in_order else -1
    prev_id = ids_in_order[idx - 1] if idx > 0 else None
    next_id = ids_in_order[idx + 1] if 0 <= idx < len(ids_in_order) - 1 else None

    progress = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id
        )
    )
    unit = db.get(Unit, lesson.unit_id)
    return LessonDetail(
        id=lesson.id,
        course_id=course.id,
        unit_id=lesson.unit_id,
        unit_title=unit.title if unit else "",
        slug=lesson.slug,
        title=lesson.title,
        description=lesson.description,
        objectives=lesson.objectives,
        cefr_level=lesson.cefr_level,
        position=lesson.position,
        estimated_minutes=lesson.estimated_minutes,
        content_version=lesson.content_version,
        is_published=lesson.status == PUBLISHED,
        content=lesson.content,
        items=items,
        exercises=exercises,
        episodes=episodes,
        media=media_refs(db, ids),
        progress=progress_out(db, progress),
        previous_lesson_id=prev_id,
        next_lesson_id=next_id,
    )
