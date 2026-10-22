"""Read models for dashboards and progress reports — all built from persisted data."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    Course,
    Enrollment,
    Exercise,
    ExerciseLearningItem,
    LearnerMastery,
    LearningItem,
    Lesson,
    LessonProgress,
    ReviewQueue,
    User,
)
from app.models.enums import (
    EnrollmentStatus,
    ExerciseType,
    LessonProgressStatus,
    PublicationStatus,
)
from app.schemas.curriculum import (
    Achievement,
    Dashboard,
    LearningItemOut,
    LessonProgressRow,
    MasteryOut,
    ProgressReport,
    ReviewEntry,
)
from app.services import curriculum
from app.services.learning import MASTERED_THRESHOLD


def progress_report(db: Session, user_id: uuid.UUID) -> ProgressReport:
    rows = db.execute(
        select(LessonProgress, Lesson.title)
        .join(Lesson, Lesson.id == LessonProgress.lesson_id)
        .where(LessonProgress.user_id == user_id)
        .order_by(LessonProgress.started_at)
    ).all()
    lessons = []
    for progress, title in rows:
        base = curriculum.progress_out(db, progress)
        lessons.append(
            LessonProgressRow(**base.model_dump(), lesson_id=progress.lesson_id, lesson_title=title)
        )

    mastery_rows = db.execute(
        select(LearnerMastery, LearningItem, ReviewQueue.due_at)
        .join(LearningItem, LearningItem.id == LearnerMastery.learning_item_id)
        .outerjoin(
            ReviewQueue,
            (ReviewQueue.user_id == LearnerMastery.user_id)
            & (ReviewQueue.learning_item_id == LearnerMastery.learning_item_id),
        )
        .where(LearnerMastery.user_id == user_id)
        .order_by(LearnerMastery.mastery.desc(), LearningItem.text)
    ).all()
    mastery = [
        MasteryOut(
            item=LearningItemOut.model_validate(item),
            attempts=m.attempts,
            correct=m.correct,
            incorrect=m.incorrect,
            recognition_correct=m.recognition_correct,
            recall_correct=m.recall_correct,
            mastery=m.mastery,
            mastered=m.mastery >= MASTERED_THRESHOLD,
            last_practiced_at=m.last_practiced_at,
            next_review_at=due,
        )
        for m, item, due in mastery_rows
    ]
    return ProgressReport(lessons=lessons, mastery=mastery)


def due_reviews(db: Session, user: User, limit: int) -> list[ReviewEntry]:
    """Due items, oldest first, each with one objective exercise from a published lesson
    that practises it (preferring recall exercises for items already recognised)."""
    now = datetime.now(UTC)
    rows = db.execute(
        select(ReviewQueue, LearningItem)
        .join(LearningItem, LearningItem.id == ReviewQueue.learning_item_id)
        .where(ReviewQueue.user_id == user.id, ReviewQueue.due_at <= now)
        .order_by(ReviewQueue.due_at)
        .limit(limit)
    ).all()
    entries: list[ReviewEntry] = []
    used: set[uuid.UUID] = set()
    for entry, item in rows:
        candidates = db.scalars(
            select(Exercise)
            .join(ExerciseLearningItem, ExerciseLearningItem.exercise_id == Exercise.id)
            .join(Lesson, Lesson.id == Exercise.lesson_id)
            .where(
                ExerciseLearningItem.learning_item_id == item.id,
                Lesson.status == PublicationStatus.PUBLISHED,
                Exercise.is_scored.is_(True),
                Exercise.type != ExerciseType.SPEAKING,
            )
            .order_by(Exercise.recall_mode.desc(), Exercise.position)
        ).all()
        accessible = []
        for ex in candidates:
            if ex.id in used:
                continue
            lesson = db.get(Lesson, ex.lesson_id)
            course = curriculum.course_of_lesson(db, lesson)
            if curriculum.active_enrollment(db, user.id, course.id) is not None:
                accessible.append(ex)
        exercise = accessible[0] if accessible else None
        if exercise:
            used.add(exercise.id)
        entries.append(
            ReviewEntry(
                item=LearningItemOut.model_validate(item),
                due_at=entry.due_at,
                exercise=curriculum.exercise_public(exercise) if exercise else None,
                lesson_id=exercise.lesson_id if exercise else None,
            )
        )
    return entries


def dashboard(db: Session, user: User) -> Dashboard:
    enrollment = db.scalar(
        select(Enrollment)
        .join(Course, Course.id == Enrollment.course_id)
        .where(
            Enrollment.user_id == user.id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
            Course.status == PublicationStatus.PUBLISHED,
        )
        .order_by(Enrollment.created_at)
    )
    course_tree = None
    current = None
    total = 0
    progress = curriculum.progress_map(db, user.id)
    if enrollment:
        course = db.get(Course, enrollment.course_id)
        course_tree = curriculum.course_tree(db, course, user, enrollment)
        lessons = curriculum.ordered_lessons(db, course.id, published_only=True)
        total = len(lessons)
        by_id = {lsn.id: lsn for lsn in lessons}
        target = by_id.get(enrollment.current_lesson_id) if enrollment.current_lesson_id else None
        if target is None or (
            progress.get(target.id) and progress[target.id].status == LessonProgressStatus.COMPLETED
        ):
            # First lesson that is not completed yet.
            target = next(
                (
                    lsn
                    for lsn in lessons
                    if not progress.get(lsn.id)
                    or progress[lsn.id].status != LessonProgressStatus.COMPLETED
                ),
                target,
            )
        if target:
            current = curriculum.lesson_summary(target, progress.get(target.id))

    completed = sum(1 for p in progress.values() if p.status == LessonProgressStatus.COMPLETED)
    practiced = db.scalar(
        select(func.count()).where(LearnerMastery.user_id == user.id, LearnerMastery.attempts > 0)
    )
    mastered = db.scalar(
        select(func.count()).where(
            LearnerMastery.user_id == user.id, LearnerMastery.mastery >= MASTERED_THRESHOLD
        )
    )
    due = db.scalar(
        select(func.count()).where(
            ReviewQueue.user_id == user.id, ReviewQueue.due_at <= datetime.now(UTC)
        )
    )
    perfect_quiz = any((p.best_quiz_percent or 0) >= 100 for p in progress.values())
    achievements = [
        Achievement(key="first_lesson", title="First lesson finished", earned=completed >= 1),
        Achievement(key="five_lessons", title="Five lessons finished", earned=completed >= 5),
        Achievement(key="ten_words", title="Practised 10 words", earned=(practiced or 0) >= 10),
        Achievement(
            key="first_mastered", title="First word you know well", earned=(mastered or 0) >= 1
        ),
        Achievement(key="perfect_quiz", title="A perfect quiz", earned=perfect_quiz),
    ]
    return Dashboard(
        display_name=user.display_name,
        course=course_tree,
        current_lesson=current,
        lessons_completed=completed,
        lessons_total=total,
        items_practiced=practiced or 0,
        items_mastered=mastered or 0,
        reviews_due=due or 0,
        last_activity_at=user.last_activity_at,
        achievements=achievements,
    )
