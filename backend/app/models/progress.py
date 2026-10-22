import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, Timestamps, UUIDPk, str_enum
from app.models.enums import CefrLevel, EnrollmentStatus, LessonProgressStatus


class Enrollment(UUIDPk, Timestamps, Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "course_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    current_level: Mapped[CefrLevel] = mapped_column(
        str_enum(CefrLevel, "cefr_level"), nullable=False, default=CefrLevel.A1
    )
    current_lesson_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL")
    )
    status: Mapped[EnrollmentStatus] = mapped_column(
        str_enum(EnrollmentStatus, "enrollment_status"),
        nullable=False,
        default=EnrollmentStatus.ACTIVE,
    )


class LessonProgress(UUIDPk, Timestamps, Base):
    """Lesson *completion* state. Learning *mastery* is tracked separately in LearnerMastery."""

    __tablename__ = "lesson_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id"),
        CheckConstraint("score >= 0 AND score <= max_score", name="score_in_range"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[LessonProgressStatus] = mapped_column(
        str_enum(LessonProgressStatus, "lesson_progress_status"),
        nullable=False,
        default=LessonProgressStatus.NOT_STARTED,
    )
    lesson_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    best_quiz_percent: Mapped[float | None] = mapped_column(Float)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ExerciseAttempt(UUIDPk, Base):
    """Immutable record of one submitted answer, with the exercise version it was scored on."""

    __tablename__ = "exercise_attempts"
    __table_args__ = (
        Index("ix_exercise_attempts_user_created", "user_id", "created_at"),
        Index("ix_exercise_attempts_user_exercise", "user_id", "exercise_id"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("exercises.id", ondelete="RESTRICT"), nullable=False
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    exercise_version: Mapped[int] = mapped_column(Integer, nullable=False)
    # Snapshot of prompt/answer/points at scoring time, so history stays interpretable.
    exercise_snapshot: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    response: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    # NULL for unscored activities (e.g. speaking without automatic evaluation).
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    recording_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class LearnerMastery(UUIDPk, Timestamps, Base):
    """Per-student evidence about one learning item. Recognition and recall are separate."""

    __tablename__ = "learner_mastery"
    __table_args__ = (
        UniqueConstraint("user_id", "learning_item_id"),
        CheckConstraint("mastery >= 0 AND mastery <= 1", name="mastery_in_range"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    learning_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("learning_items.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    incorrect: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    recognition_correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    recall_correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mastery: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    last_practiced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ReviewQueue(UUIDPk, Timestamps, Base):
    """Spaced-repetition schedule for one student and one learning item."""

    __tablename__ = "review_queue"
    __table_args__ = (
        UniqueConstraint("user_id", "learning_item_id"),
        Index("ix_review_queue_user_due", "user_id", "due_at"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    learning_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("learning_items.id", ondelete="RESTRICT"), nullable=False
    )
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    interval_days: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ease: Mapped[float] = mapped_column(Float, nullable=False, default=2.3)
    repetitions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_result: Mapped[str | None] = mapped_column(String(16))


class AuditLog(UUIDPk, Base):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_entity", "entity_type", "entity_id"),)

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(64))
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
