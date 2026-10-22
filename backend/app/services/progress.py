"""Submitting exercise attempts and updating lesson progress."""

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.exercises.definitions import CHOICE_TYPES
from app.exercises.scoring import ScoreResult, score_response
from app.models import (
    Exercise,
    ExerciseAttempt,
    ExerciseLearningItem,
    Lesson,
    LessonProgress,
    MediaAsset,
    User,
)
from app.models.enums import (
    ExerciseType,
    LessonProgressStatus,
    LessonSection,
    MediaType,
    UserRole,
)
from app.schemas.curriculum import AttemptResult
from app.services import curriculum, learning

SOLUTION_AFTER_WRONG_TRIES = 2


def _solution(exercise: Exercise) -> dict[str, Any]:
    answer = exercise.answer
    t = exercise.type
    if t in CHOICE_TYPES or t == ExerciseType.TRUE_FALSE:
        return {"correct": answer["correct"]}
    if t == ExerciseType.SENTENCE_BUILDER:
        return {"sentence": answer["accepted"][0]}
    if t == ExerciseType.FILL_BLANK:
        return {"blanks": [options[0] for options in answer["blanks"]]}
    return dict(answer)


def _snapshot(exercise: Exercise) -> dict[str, Any]:
    return {
        "type": exercise.type.value,
        "instructions": exercise.instructions,
        "prompt": exercise.prompt,
        "answer": exercise.answer,
        "points": exercise.points,
        "is_scored": exercise.is_scored,
    }


def get_or_create_progress(db: Session, user_id: uuid.UUID, lesson: Lesson) -> LessonProgress:
    progress = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user_id, LessonProgress.lesson_id == lesson.id
        )
    )
    if progress is None:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson.id,
            status=LessonProgressStatus.NOT_STARTED,
            lesson_version=lesson.content_version,
            score=0,
            max_score=0,
        )
        db.add(progress)
    return progress


def start_lesson(db: Session, user: User, lesson: Lesson) -> LessonProgress:
    progress = get_or_create_progress(db, user.id, lesson)
    now = datetime.now(UTC)
    if progress.status == LessonProgressStatus.NOT_STARTED:
        progress.status = LessonProgressStatus.IN_PROGRESS
        progress.started_at = now
    progress.last_activity_at = now
    _set_current_lesson(db, user, lesson)
    db.commit()
    return progress


def _set_current_lesson(db: Session, user: User, lesson: Lesson) -> None:
    course = curriculum.course_of_lesson(db, lesson)
    enrollment = curriculum.active_enrollment(db, user.id, course.id)
    if enrollment:
        enrollment.current_lesson_id = lesson.id


def _recalculate(db: Session, progress: LessonProgress, lesson: Lesson, now: datetime) -> None:
    """Score = best score per current exercise. Completed once every exercise was tried."""
    best = dict(
        db.execute(
            select(ExerciseAttempt.exercise_id, func.max(ExerciseAttempt.score))
            .where(
                ExerciseAttempt.user_id == progress.user_id,
                ExerciseAttempt.lesson_id == lesson.id,
            )
            .group_by(ExerciseAttempt.exercise_id)
        ).all()
    )
    scored = [e for e in lesson.exercises if e.is_scored and e.type != ExerciseType.SPEAKING]
    progress.max_score = sum(e.points for e in scored)
    progress.score = min(progress.max_score, sum(best.get(e.id, 0) for e in scored))
    quiz = [e for e in scored if e.section == LessonSection.QUIZ]
    quiz_max = sum(e.points for e in quiz)
    if quiz_max and all(e.id in best for e in quiz):
        progress.best_quiz_percent = round(100 * sum(best[e.id] for e in quiz) / quiz_max, 1)
    progress.last_activity_at = now
    if progress.status == LessonProgressStatus.NOT_STARTED:
        progress.status = LessonProgressStatus.IN_PROGRESS
        progress.started_at = now
    if progress.status != LessonProgressStatus.COMPLETED and all(
        e.id in best for e in lesson.exercises
    ):
        progress.status = LessonProgressStatus.COMPLETED
        progress.completed_at = now
        progress.lesson_version = lesson.content_version


def _advance_enrollment(db: Session, user: User, lesson: Lesson) -> None:
    course = curriculum.course_of_lesson(db, lesson)
    enrollment = curriculum.active_enrollment(db, user.id, course.id)
    if enrollment is None:
        return
    sequence = curriculum.ordered_lessons(db, course.id, published_only=True)
    ids = [lsn.id for lsn in sequence]
    if lesson.id in ids and ids.index(lesson.id) + 1 < len(ids):
        enrollment.current_lesson_id = ids[ids.index(lesson.id) + 1]


def submit_attempt(
    db: Session, user: User, exercise_id: uuid.UUID, response: dict[str, Any]
) -> AttemptResult:
    if user.role != UserRole.STUDENT:
        raise AppError(403, "Only students submit answers. Admin preview does not save attempts.")
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        raise AppError(404, "Exercise not found.")
    lesson, _ = curriculum.get_accessible_lesson(db, user, exercise.lesson_id)

    try:
        result: ScoreResult = score_response(
            exercise.type, exercise.answer, response, exercise.points, exercise.is_scored
        )
    except ValidationError as exc:
        raise AppError(
            422,
            "This answer has the wrong format.",
            details=[{"loc": list(e["loc"]), "msg": e["msg"]} for e in exc.errors()],
        ) from exc

    recording_id = response.get("recording_asset_id")
    if recording_id:
        asset = db.get(MediaAsset, uuid.UUID(str(recording_id)))
        if asset is None or asset.uploaded_by_id != user.id or asset.media_type != MediaType.AUDIO:
            raise AppError(404, "Recording not found.")

    now = datetime.now(UTC)
    last_at = db.scalar(
        select(func.max(ExerciseAttempt.created_at)).where(
            ExerciseAttempt.user_id == user.id, ExerciseAttempt.exercise_id == exercise.id
        )
    )
    wrong_before = db.scalar(
        select(func.count()).where(
            ExerciseAttempt.user_id == user.id,
            ExerciseAttempt.exercise_id == exercise.id,
            ExerciseAttempt.is_correct.is_(False),
        )
    )
    is_fresh = last_at is None or now - last_at > learning.RETRY_WINDOW
    counted = is_fresh and result.is_correct is not None

    attempt = ExerciseAttempt(
        user_id=user.id,
        exercise_id=exercise.id,
        lesson_id=lesson.id,
        exercise_version=exercise.version,
        exercise_snapshot=_snapshot(exercise),
        response=response,
        is_correct=result.is_correct,
        score=result.score,
        max_score=result.max_score,
        recording_asset_id=uuid.UUID(str(recording_id)) if recording_id else None,
        created_at=now,
    )
    db.add(attempt)

    if counted:
        item_ids = list(
            db.scalars(
                select(ExerciseLearningItem.learning_item_id).where(
                    ExerciseLearningItem.exercise_id == exercise.id
                )
            )
        )
        learning.record_evidence(
            db, user.id, item_ids, bool(result.is_correct), exercise.recall_mode, now
        )

    progress = get_or_create_progress(db, user.id, lesson)
    db.flush()
    was_completed = progress.status == LessonProgressStatus.COMPLETED
    _recalculate(db, progress, lesson, now)
    if not was_completed and progress.status == LessonProgressStatus.COMPLETED:
        _advance_enrollment(db, user, lesson)
    user.last_activity_at = now
    db.commit()

    fb = exercise.feedback or {}
    wrong_total = (wrong_before or 0) + (1 if result.is_correct is False else 0)
    reveal = result.is_correct is True or wrong_total >= SOLUTION_AFTER_WRONG_TRIES
    if result.is_correct is None:
        message = fb.get("correct") or "Great job practising! Listen and compare with the model."
    elif result.is_correct:
        message = fb.get("correct") or "Well done!"
    else:
        message = fb.get("incorrect") or "Not quite. Try again!"
    return AttemptResult(
        attempt_id=attempt.id,
        is_correct=result.is_correct,
        score=result.score,
        max_score=result.max_score,
        message=message,
        explanation=fb.get("explanation") if reveal else fb.get("hint"),
        details=result.details,
        solution=_solution(exercise) if reveal and result.is_correct is not None else None,
        counted_for_mastery=counted,
        lesson_progress=curriculum.progress_out(db, progress),
    )
