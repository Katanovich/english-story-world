"""Schemas for the admin CMS."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import (
    AccountStatus,
    CefrLevel,
    ExerciseType,
    LearningItemKind,
    LessonItemRole,
    LessonSection,
    PublicationStatus,
    RecallMode,
)
from app.schemas.common import ApiModel, OrmModel

SLUG = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
KEY = r"^[a-z0-9_.-]+$"


# ---- Curriculum tree ------------------------------------------------------------------


class LessonNode(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    status: PublicationStatus
    position: int
    content_version: int
    exercise_count: int


class UnitNode(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str
    position: int
    lessons: list[LessonNode]


class LevelNode(BaseModel):
    id: uuid.UUID
    cefr_level: CefrLevel
    title: str
    description: str
    position: int
    units: list[UnitNode]


class CourseNode(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str
    status: PublicationStatus
    levels: list[LevelNode]


class CourseIn(ApiModel):
    slug: str = Field(pattern=SLUG, max_length=80)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class CourseUpdate(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: PublicationStatus | None = None


class LevelIn(ApiModel):
    cefr_level: CefrLevel
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    position: int = Field(default=0, ge=0)


class LevelUpdate(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    position: int | None = Field(default=None, ge=0)


class UnitIn(ApiModel):
    slug: str = Field(pattern=SLUG, max_length=80)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    position: int = Field(default=0, ge=0)


class UnitUpdate(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    position: int | None = Field(default=None, ge=0)


# ---- Lessons --------------------------------------------------------------------------


class LessonIn(ApiModel):
    slug: str = Field(pattern=SLUG, max_length=80)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    position: int = Field(default=0, ge=0)
    estimated_minutes: int = Field(default=20, ge=1, le=240)


class LessonUpdate(ApiModel):
    slug: str | None = Field(default=None, pattern=SLUG, max_length=80)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    objectives: list[str] | None = Field(default=None, max_length=20)
    position: int | None = Field(default=None, ge=0)
    estimated_minutes: int | None = Field(default=None, ge=1, le=240)
    content: dict[str, Any] | None = None
    cover_image_id: uuid.UUID | None = None


class ItemLink(ApiModel):
    learning_item_id: uuid.UUID
    role: LessonItemRole


class ExerciseAdmin(OrmModel):
    id: uuid.UUID
    lesson_id: uuid.UUID
    key: str
    type: ExerciseType
    section: LessonSection
    recall_mode: RecallMode
    position: int
    instructions: str
    prompt: dict[str, Any]
    answer: dict[str, Any]
    feedback: dict[str, Any]
    points: int
    is_scored: bool
    image_id: uuid.UUID | None
    audio_id: uuid.UUID | None
    version: int
    learning_item_ids: list[uuid.UUID] = Field(default_factory=list)
    attempt_count: int = 0


class ExerciseIn(ApiModel):
    key: str = Field(pattern=KEY, max_length=80)
    type: ExerciseType
    section: LessonSection
    recall_mode: RecallMode = RecallMode.RECOGNITION
    position: int = Field(default=0, ge=0)
    instructions: str = Field(min_length=1, max_length=500)
    prompt: dict[str, Any]
    answer: dict[str, Any]
    feedback: dict[str, str] = Field(default_factory=dict)
    points: int = Field(default=1, ge=0, le=20)
    image_id: uuid.UUID | None = None
    audio_id: uuid.UUID | None = None
    learning_item_ids: list[uuid.UUID] = Field(default_factory=list)


class ExerciseUpdate(ApiModel):
    key: str | None = Field(default=None, pattern=KEY, max_length=80)
    type: ExerciseType | None = None
    section: LessonSection | None = None
    recall_mode: RecallMode | None = None
    position: int | None = Field(default=None, ge=0)
    instructions: str | None = Field(default=None, min_length=1, max_length=500)
    prompt: dict[str, Any] | None = None
    answer: dict[str, Any] | None = None
    feedback: dict[str, str] | None = None
    points: int | None = Field(default=None, ge=0, le=20)
    image_id: uuid.UUID | None = None
    audio_id: uuid.UUID | None = None
    learning_item_ids: list[uuid.UUID] | None = None


class EpisodeIn(ApiModel):
    title: str = Field(min_length=1, max_length=200)
    synopsis: str = Field(default="", max_length=2000)
    position: int = Field(default=1, ge=0)


class EpisodeUpdate(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    synopsis: str | None = Field(default=None, max_length=2000)
    position: int | None = Field(default=None, ge=0)
    status: PublicationStatus | None = None


class EpisodeAdmin(OrmModel):
    id: uuid.UUID
    title: str
    synopsis: str
    position: int
    status: PublicationStatus
    video_asset_id: uuid.UUID | None
    subtitle_asset_id: uuid.UUID | None
    poster_image_id: uuid.UUID | None


class LessonAdmin(BaseModel):
    id: uuid.UUID
    unit_id: uuid.UUID
    course_id: uuid.UUID
    slug: str
    title: str
    description: str
    objectives: list[str]
    cefr_level: CefrLevel
    position: int
    estimated_minutes: int
    content: dict[str, Any]
    status: PublicationStatus
    content_version: int
    cover_image_id: uuid.UUID | None
    updated_at: datetime
    items: list[ItemLink]
    exercises: list[ExerciseAdmin]
    episodes: list[EpisodeAdmin]


class ValidationReport(BaseModel):
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


# ---- Learning items -------------------------------------------------------------------


class LearningItemAdmin(OrmModel):
    id: uuid.UUID
    key: str
    kind: LearningItemKind
    text: str
    emoji: str | None
    translation_ru: str | None
    explanation: str | None
    cefr_level: CefrLevel
    examples: list[str]
    introduced_in_lesson_id: uuid.UUID | None
    image_id: uuid.UUID | None
    audio_id: uuid.UUID | None


class LearningItemIn(ApiModel):
    key: str = Field(pattern=KEY, max_length=120)
    kind: LearningItemKind
    text: str = Field(min_length=1, max_length=255)
    emoji: str | None = Field(default=None, max_length=16)
    translation_ru: str | None = Field(default=None, max_length=255)
    explanation: str | None = Field(default=None, max_length=2000)
    cefr_level: CefrLevel = CefrLevel.A1
    examples: list[str] = Field(default_factory=list, max_length=10)
    introduced_in_lesson_id: uuid.UUID | None = None
    image_id: uuid.UUID | None = None
    audio_id: uuid.UUID | None = None


class LearningItemUpdate(ApiModel):
    text: str | None = Field(default=None, min_length=1, max_length=255)
    kind: LearningItemKind | None = None
    emoji: str | None = Field(default=None, max_length=16)
    translation_ru: str | None = Field(default=None, max_length=255)
    explanation: str | None = Field(default=None, max_length=2000)
    cefr_level: CefrLevel | None = None
    examples: list[str] | None = Field(default=None, max_length=10)
    introduced_in_lesson_id: uuid.UUID | None = None
    image_id: uuid.UUID | None = None
    audio_id: uuid.UUID | None = None


# ---- Overview & audit -----------------------------------------------------------------


class AuditEntry(OrmModel):
    id: uuid.UUID
    actor_id: uuid.UUID | None
    actor_username: str | None = None
    action: str
    entity_type: str
    entity_id: str | None
    details: dict[str, Any]
    created_at: datetime


class Overview(BaseModel):
    students_by_status: dict[AccountStatus, int]
    lessons_published: int
    lessons_draft: int
    learning_items: int
    media_assets: int
    attempts_last_7_days: int
    active_students_last_7_days: int
