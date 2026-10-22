"""Import every model so Base.metadata is complete (needed by Alembic)."""

from app.db.base import Base
from app.models.curriculum import (
    Course,
    CourseLevel,
    Exercise,
    ExerciseLearningItem,
    LearningItem,
    Lesson,
    LessonLearningItem,
    StoryEpisode,
    Unit,
)
from app.models.media import MediaAsset
from app.models.progress import (
    AuditLog,
    Enrollment,
    ExerciseAttempt,
    LearnerMastery,
    LessonProgress,
    ReviewQueue,
)
from app.models.user import AuthSession, PasswordResetToken, User

__all__ = [
    "AuditLog",
    "AuthSession",
    "Base",
    "Course",
    "CourseLevel",
    "Enrollment",
    "Exercise",
    "ExerciseAttempt",
    "ExerciseLearningItem",
    "LearnerMastery",
    "LearningItem",
    "Lesson",
    "LessonLearningItem",
    "LessonProgress",
    "MediaAsset",
    "PasswordResetToken",
    "ReviewQueue",
    "StoryEpisode",
    "Unit",
    "User",
]
