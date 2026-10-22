"""Admin: enrolments and inspection of a student's learning progress."""

import uuid

from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import AdminUser, DbSession
from app.api.routes.admin_users import _get_student
from app.core.errors import AppError
from app.models import Course, Enrollment, ExerciseAttempt
from app.models.enums import EnrollmentStatus
from app.schemas.curriculum import (
    AttemptOut,
    EnrollmentOut,
    EnrollmentSet,
    StudentProgressAdmin,
)
from app.services import audit, reports

router = APIRouter(prefix="/admin/students", tags=["admin: students"])


@router.put("/{student_id}/enrollment", response_model=EnrollmentOut)
def set_enrollment(student_id: uuid.UUID, body: EnrollmentSet, db: DbSession, admin: AdminUser):
    """Assign a course and level. Re-assigning keeps all existing progress."""
    student = _get_student(db, student_id)
    if db.get(Course, body.course_id) is None:
        raise AppError(404, "Course not found.")
    enrollment = db.scalar(
        select(Enrollment).where(
            Enrollment.user_id == student.id, Enrollment.course_id == body.course_id
        )
    )
    if enrollment is None:
        enrollment = Enrollment(user_id=student.id, course_id=body.course_id)
        db.add(enrollment)
    enrollment.current_level = body.cefr_level
    enrollment.status = EnrollmentStatus.ACTIVE
    audit.record(
        db,
        admin.id,
        "student.enroll",
        "user",
        student.id,
        {"course_id": str(body.course_id), "level": body.cefr_level},
    )
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/{student_id}/progress", response_model=StudentProgressAdmin)
def student_progress(student_id: uuid.UUID, db: DbSession, _: AdminUser):
    student = _get_student(db, student_id)
    report = reports.progress_report(db, student.id)
    enrollments = db.scalars(select(Enrollment).where(Enrollment.user_id == student.id)).all()
    attempts = db.scalars(
        select(ExerciseAttempt)
        .where(ExerciseAttempt.user_id == student.id)
        .order_by(ExerciseAttempt.created_at.desc())
        .limit(50)
    ).all()
    return StudentProgressAdmin(
        **report.model_dump(),
        enrollments=[EnrollmentOut.model_validate(e) for e in enrollments],
        recent_attempts=[AttemptOut.model_validate(a) for a in attempts],
    )
