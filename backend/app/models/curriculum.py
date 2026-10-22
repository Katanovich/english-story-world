import uuid
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, Timestamps, UUIDPk, str_enum
from app.models.enums import (
    CefrLevel,
    ExerciseType,
    LearningItemKind,
    LessonItemRole,
    LessonSection,
    PublicationStatus,
    RecallMode,
)


class Course(UUIDPk, Timestamps, Base):
    __tablename__ = "courses"

    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[PublicationStatus] = mapped_column(
        str_enum(PublicationStatus, "publication_status"),
        nullable=False,
        default=PublicationStatus.DRAFT,
    )

    levels: Mapped[list["CourseLevel"]] = relationship(
        back_populates="course", order_by="CourseLevel.position", cascade="all, delete-orphan"
    )


class CourseLevel(UUIDPk, Timestamps, Base):
    __tablename__ = "course_levels"
    __table_args__ = (UniqueConstraint("course_id", "cefr_level"),)

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cefr_level: Mapped[CefrLevel] = mapped_column(str_enum(CefrLevel, "cefr_level"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    course: Mapped[Course] = relationship(back_populates="levels")
    units: Mapped[list["Unit"]] = relationship(
        back_populates="level", order_by="Unit.position", cascade="all, delete-orphan"
    )


class Unit(UUIDPk, Timestamps, Base):
    __tablename__ = "units"
    __table_args__ = (UniqueConstraint("level_id", "slug"),)

    level_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("course_levels.id", ondelete="CASCADE"), nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    level: Mapped[CourseLevel] = relationship(back_populates="units")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="unit", order_by="Lesson.position", cascade="all, delete-orphan"
    )


class Lesson(UUIDPk, Timestamps, Base):
    """A lesson. Structured rich content (reading, listening, speaking) lives in `content`.

    `content_version` increases every time the lesson is published with changes so that
    progress rows can record which version a learner completed.
    """

    __tablename__ = "lessons"
    __table_args__ = (
        UniqueConstraint("unit_id", "slug"),
        CheckConstraint("estimated_minutes > 0", name="estimated_minutes_positive"),
        CheckConstraint("content_version >= 1", name="content_version_positive"),
        Index("ix_lessons_unit_position", "unit_id", "position"),
    )

    unit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("units.id", ondelete="CASCADE"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    objectives: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    cefr_level: Mapped[CefrLevel] = mapped_column(str_enum(CefrLevel, "cefr_level"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    # {reading: {...}, listening: [...], speaking_prompts: [...], grammar_notes: [...]}
    content: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[PublicationStatus] = mapped_column(
        str_enum(PublicationStatus, "publication_status"),
        nullable=False,
        default=PublicationStatus.DRAFT,
        index=True,
    )
    content_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    cover_image_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )

    unit: Mapped[Unit] = relationship(back_populates="lessons")
    exercises: Mapped[list["Exercise"]] = relationship(
        back_populates="lesson", order_by="Exercise.position", cascade="all, delete-orphan"
    )
    item_links: Mapped[list["LessonLearningItem"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )
    episodes: Mapped[list["StoryEpisode"]] = relationship(
        back_populates="lesson", order_by="StoryEpisode.position", cascade="all, delete-orphan"
    )


class LearningItem(UUIDPk, Timestamps, Base):
    """A reusable unit of knowledge (word, phrase, grammar pattern...) with a stable key."""

    __tablename__ = "learning_items"

    key: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    kind: Mapped[LearningItemKind] = mapped_column(
        str_enum(LearningItemKind, "learning_item_kind"), nullable=False, index=True
    )
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    emoji: Mapped[str | None] = mapped_column(String(16))
    translation_ru: Mapped[str | None] = mapped_column(String(255))
    explanation: Mapped[str | None] = mapped_column(Text)
    cefr_level: Mapped[CefrLevel] = mapped_column(str_enum(CefrLevel, "cefr_level"), nullable=False)
    examples: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    introduced_in_lesson_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"), index=True
    )
    image_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    audio_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )


class LessonLearningItem(Base):
    """Links a lesson to the items it teaches (NEW) or reviews (RECENT/OLDER_REVIEW)."""

    __tablename__ = "lesson_learning_items"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True
    )
    learning_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("learning_items.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    role: Mapped[LessonItemRole] = mapped_column(
        str_enum(LessonItemRole, "lesson_item_role"), nullable=False
    )

    lesson: Mapped[Lesson] = relationship(back_populates="item_links")
    learning_item: Mapped[LearningItem] = relationship()


class Exercise(UUIDPk, Timestamps, Base):
    """One exercise. `prompt` is safe to send to learners; `answer` never leaves the server
    before an attempt is submitted."""

    __tablename__ = "exercises"
    __table_args__ = (
        UniqueConstraint("lesson_id", "key"),
        CheckConstraint("points >= 0", name="points_non_negative"),
        CheckConstraint("version >= 1", name="version_positive"),
        Index("ix_exercises_lesson_position", "lesson_id", "position"),
    )

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    key: Mapped[str] = mapped_column(String(80), nullable=False)
    type: Mapped[ExerciseType] = mapped_column(
        str_enum(ExerciseType, "exercise_type"), nullable=False
    )
    section: Mapped[LessonSection] = mapped_column(
        str_enum(LessonSection, "lesson_section"), nullable=False
    )
    recall_mode: Mapped[RecallMode] = mapped_column(
        str_enum(RecallMode, "recall_mode"), nullable=False, default=RecallMode.RECOGNITION
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    prompt: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    answer: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    feedback: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_scored: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    image_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    audio_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    lesson: Mapped[Lesson] = relationship(back_populates="exercises")
    item_links: Mapped[list["ExerciseLearningItem"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )


class ExerciseLearningItem(Base):
    __tablename__ = "exercise_learning_items"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True
    )
    learning_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("learning_items.id", ondelete="CASCADE"), primary_key=True, index=True
    )

    exercise: Mapped[Exercise] = relationship(back_populates="item_links")
    learning_item: Mapped[LearningItem] = relationship()


class StoryEpisode(UUIDPk, Timestamps, Base):
    """A cartoon episode attached to a lesson. The video is optional until it is produced."""

    __tablename__ = "story_episodes"
    __table_args__ = (UniqueConstraint("lesson_id", "position"),)

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    synopsis: Mapped[str] = mapped_column(Text, nullable=False, default="")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    video_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    subtitle_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    poster_image_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("media_assets.id", ondelete="SET NULL")
    )
    status: Mapped[PublicationStatus] = mapped_column(
        str_enum(PublicationStatus, "publication_status"),
        nullable=False,
        default=PublicationStatus.DRAFT,
    )

    lesson: Mapped[Lesson] = relationship(back_populates="episodes")
