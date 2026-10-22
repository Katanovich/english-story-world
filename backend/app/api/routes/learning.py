"""Learner-facing routes: lessons, exercise submissions, own progress, review, recordings."""

import uuid

from fastapi import APIRouter, File, Query, UploadFile, status
from sqlalchemy import func, select

from app.api.deps import CurrentUser, DbSession, StudentUser
from app.core.errors import AppError
from app.models import Course, Enrollment, ExerciseAttempt
from app.models.enums import EnrollmentStatus, MediaType, PublicationStatus
from app.schemas.common import Page
from app.schemas.curriculum import (
    AttemptOut,
    AttemptResult,
    AttemptSubmit,
    CourseTree,
    Dashboard,
    EpisodeListItem,
    LessonDetail,
    LessonProgressOut,
    MediaRef,
    ProgressReport,
    ReviewEntry,
)
from app.services import curriculum, reports
from app.services import media as media_service
from app.services import progress as progress_service

router = APIRouter(tags=["learning"])


@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
def get_lesson(lesson_id: uuid.UUID, db: DbSession, user: CurrentUser):
    """Students: published lessons of their courses. Admins: any lesson (preview)."""
    lesson, course = curriculum.get_accessible_lesson(db, user, lesson_id)
    return curriculum.lesson_detail(db, user, lesson, course)


@router.post("/lessons/{lesson_id}/start", response_model=LessonProgressOut)
def start_lesson(lesson_id: uuid.UUID, db: DbSession, user: StudentUser):
    lesson, _ = curriculum.get_accessible_lesson(db, user, lesson_id)
    progress = progress_service.start_lesson(db, user, lesson)
    return curriculum.progress_out(db, progress)


@router.post(
    "/exercises/{exercise_id}/attempts",
    response_model=AttemptResult,
    status_code=status.HTTP_201_CREATED,
)
def submit_attempt(exercise_id: uuid.UUID, body: AttemptSubmit, db: DbSession, user: StudentUser):
    return progress_service.submit_attempt(db, user, exercise_id, body.response)


me = APIRouter(prefix="/me", tags=["me"])


@me.get("/dashboard", response_model=Dashboard)
def my_dashboard(db: DbSession, user: StudentUser):
    return reports.dashboard(db, user)


@me.get("/courses", response_model=list[CourseTree])
def my_courses(db: DbSession, user: StudentUser):
    rows = db.execute(
        select(Course, Enrollment)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .where(
            Enrollment.user_id == user.id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
            Course.status == PublicationStatus.PUBLISHED,
        )
        .order_by(Course.title)
    ).all()
    return [curriculum.course_tree(db, c, user, e) for c, e in rows]


@me.get("/progress", response_model=ProgressReport)
def my_progress(db: DbSession, user: StudentUser):
    return reports.progress_report(db, user.id)


@me.get("/review", response_model=list[ReviewEntry])
def my_review_queue(db: DbSession, user: StudentUser, limit: int = Query(default=10, ge=1, le=30)):
    return reports.due_reviews(db, user, limit)


@me.get("/attempts", response_model=Page[AttemptOut])
def my_attempts(
    db: DbSession,
    user: StudentUser,
    lesson_id: uuid.UUID | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    stmt = select(ExerciseAttempt).where(ExerciseAttempt.user_id == user.id)
    if lesson_id:
        stmt = stmt.where(ExerciseAttempt.lesson_id == lesson_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(ExerciseAttempt.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)


@me.post("/recordings", response_model=MediaRef, status_code=status.HTTP_201_CREATED)
def upload_recording(db: DbSession, user: StudentUser, file: UploadFile = File(...)):
    """Voice recording for a speaking exercise. Stored privately; never sent to external
    services. Visible only to the student and administrators."""
    if file.filename is None:
        raise AppError(422, "A file is required.")
    asset = media_service.store_upload(
        db, uploader=user, filename=file.filename, stream=file.file, media_type=MediaType.AUDIO
    )
    db.commit()
    return MediaRef.model_validate(asset)


@me.get("/episodes", response_model=list[EpisodeListItem])
def my_episodes(db: DbSession, user: StudentUser):
    """Published story episodes of published lessons in the student's courses."""
    course_ids = db.scalars(
        select(Enrollment.course_id)
        .join(Course, Course.id == Enrollment.course_id)
        .where(
            Enrollment.user_id == user.id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
            Course.status == PublicationStatus.PUBLISHED,
        )
    ).all()
    result: list[EpisodeListItem] = []
    for course_id in course_ids:
        for lesson in curriculum.ordered_lessons(db, course_id, published_only=True):
            for ep in lesson.episodes:
                if ep.status != PublicationStatus.PUBLISHED:
                    continue
                result.append(
                    EpisodeListItem(
                        id=ep.id,
                        title=ep.title,
                        synopsis=ep.synopsis,
                        position=ep.position,
                        video_asset_id=ep.video_asset_id,
                        subtitle_asset_id=ep.subtitle_asset_id,
                        poster_image_id=ep.poster_image_id,
                        has_video=ep.video_asset_id is not None,
                        lesson_id=lesson.id,
                        lesson_title=lesson.title,
                        lesson_position=lesson.position,
                    )
                )
    return result
