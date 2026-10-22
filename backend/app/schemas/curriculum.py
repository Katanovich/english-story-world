import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, computed_field

from app.core.config import get_settings
from app.models.enums import (
    CefrLevel,
    ExerciseType,
    LearningItemKind,
    LessonItemRole,
    LessonProgressStatus,
    LessonSection,
    MediaStatus,
    MediaType,
    RecallMode,
)
from app.schemas.common import ApiModel, OrmModel


class MediaRef(OrmModel):
    id: uuid.UUID
    media_type: MediaType
    mime_type: str
    status: MediaStatus
    alt_text: str | None = None
    duration_seconds: float | None = None
    subtitle_asset_id: uuid.UUID | None = None
    transcript: str | None = None

    @computed_field
    @property
    def url(self) -> str:
        return f"{get_settings().api_prefix}/media/{self.id}"


class MediaAdminView(MediaRef):
    original_filename: str
    size_bytes: int
    storage_backend: str
    created_at: datetime


class LearningItemOut(OrmModel):
    id: uuid.UUID
    key: str
    kind: LearningItemKind
    text: str
    emoji: str | None
    translation_ru: str | None
    explanation: str | None
    examples: list[str]
    image_id: uuid.UUID | None
    audio_id: uuid.UUID | None


class LessonItemOut(BaseModel):
    role: LessonItemRole
    item: LearningItemOut


class ExercisePublic(OrmModel):
    """Learner view of an exercise: no answer key, no feedback text."""

    id: uuid.UUID
    key: str
    type: ExerciseType
    section: LessonSection
    recall_mode: RecallMode
    position: int
    instructions: str
    prompt: dict[str, Any]
    points: int
    is_scored: bool
    image_id: uuid.UUID | None
    audio_id: uuid.UUID | None
    version: int


class EpisodeOut(OrmModel):
    id: uuid.UUID
    title: str
    synopsis: str
    position: int
    video_asset_id: uuid.UUID | None
    subtitle_asset_id: uuid.UUID | None
    poster_image_id: uuid.UUID | None
    has_video: bool


class LessonProgressOut(OrmModel):
    status: LessonProgressStatus
    score: int
    max_score: int
    best_quiz_percent: float | None
    lesson_version: int
    started_at: datetime | None
    completed_at: datetime | None
    attempted_exercise_ids: list[uuid.UUID] = Field(default_factory=list)


class LessonSummary(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str
    position: int
    estimated_minutes: int
    cefr_level: CefrLevel
    cover_image_id: uuid.UUID | None
    progress_status: LessonProgressStatus


class UnitOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    lessons: list[LessonSummary]


class LevelOut(BaseModel):
    id: uuid.UUID
    cefr_level: CefrLevel
    title: str
    units: list[UnitOut]


class CourseTree(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str
    current_level: CefrLevel | None
    current_lesson_id: uuid.UUID | None
    levels: list[LevelOut]


class LessonDetail(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    unit_id: uuid.UUID
    unit_title: str
    slug: str
    title: str
    description: str
    objectives: list[str]
    cefr_level: CefrLevel
    position: int
    estimated_minutes: int
    content_version: int
    is_published: bool
    content: dict[str, Any]
    items: list[LessonItemOut]
    exercises: list[ExercisePublic]
    episodes: list[EpisodeOut]
    media: dict[str, MediaRef]
    progress: LessonProgressOut | None
    previous_lesson_id: uuid.UUID | None
    next_lesson_id: uuid.UUID | None


class AttemptSubmit(ApiModel):
    response: dict[str, Any]


class AttemptResult(BaseModel):
    attempt_id: uuid.UUID
    is_correct: bool | None
    score: int
    max_score: int
    message: str | None
    explanation: str | None
    details: dict[str, Any]
    # Revealed only after a correct answer or after repeated tries.
    solution: dict[str, Any] | None
    counted_for_mastery: bool
    lesson_progress: LessonProgressOut


class AttemptOut(OrmModel):
    id: uuid.UUID
    exercise_id: uuid.UUID
    lesson_id: uuid.UUID
    exercise_version: int
    is_correct: bool | None
    score: int
    max_score: int
    created_at: datetime


class MasteryOut(BaseModel):
    item: LearningItemOut
    attempts: int
    correct: int
    incorrect: int
    recognition_correct: int
    recall_correct: int
    mastery: float
    mastered: bool
    last_practiced_at: datetime | None
    next_review_at: datetime | None


class ReviewEntry(BaseModel):
    item: LearningItemOut
    due_at: datetime
    exercise: ExercisePublic | None
    lesson_id: uuid.UUID | None


class Achievement(BaseModel):
    key: str
    title: str
    earned: bool


class Dashboard(BaseModel):
    display_name: str
    course: CourseTree | None
    current_lesson: LessonSummary | None
    lessons_completed: int
    lessons_total: int
    items_practiced: int
    items_mastered: int
    reviews_due: int
    last_activity_at: datetime | None
    achievements: list[Achievement]


class LessonProgressRow(LessonProgressOut):
    lesson_id: uuid.UUID
    lesson_title: str


class ProgressReport(BaseModel):
    lessons: list[LessonProgressRow]
    mastery: list[MasteryOut]


class EnrollmentSet(ApiModel):
    course_id: uuid.UUID
    cefr_level: CefrLevel = CefrLevel.A1


class EnrollmentOut(OrmModel):
    id: uuid.UUID
    course_id: uuid.UUID
    current_level: CefrLevel
    current_lesson_id: uuid.UUID | None
    status: str


class StudentProgressAdmin(ProgressReport):
    enrollments: list[EnrollmentOut]
    recent_attempts: list[AttemptOut]


class EpisodeMediaSet(ApiModel):
    video_asset_id: uuid.UUID | None = None
    subtitle_asset_id: uuid.UUID | None = None
    poster_image_id: uuid.UUID | None = None


class EpisodeListItem(EpisodeOut):
    lesson_id: uuid.UUID
    lesson_title: str
    lesson_position: int
