from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"


class AccountStatus(StrEnum):
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"


class CefrLevel(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"


class PublicationStatus(StrEnum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class LearningItemKind(StrEnum):
    VOCABULARY = "VOCABULARY"
    PHRASE = "PHRASE"
    GRAMMAR = "GRAMMAR"
    PRONUNCIATION = "PRONUNCIATION"
    READING = "READING"
    LISTENING = "LISTENING"


class LessonItemRole(StrEnum):
    """How a learning item is used in a lesson (cumulative curriculum)."""

    NEW = "NEW"
    RECENT_REVIEW = "RECENT_REVIEW"
    OLDER_REVIEW = "OLDER_REVIEW"


class ExerciseType(StrEnum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    IMAGE_SELECTION = "IMAGE_SELECTION"
    MATCHING = "MATCHING"
    SENTENCE_BUILDER = "SENTENCE_BUILDER"
    FILL_BLANK = "FILL_BLANK"
    READING_COMPREHENSION = "READING_COMPREHENSION"
    LISTENING_COMPREHENSION = "LISTENING_COMPREHENSION"
    TRUE_FALSE = "TRUE_FALSE"
    ORDER_EVENTS = "ORDER_EVENTS"
    SPEAKING = "SPEAKING"


class LessonSection(StrEnum):
    VOCABULARY = "VOCABULARY"
    READING = "READING"
    LISTENING = "LISTENING"
    GRAMMAR = "GRAMMAR"
    SPEAKING = "SPEAKING"
    QUIZ = "QUIZ"


class RecallMode(StrEnum):
    """Recognition (choose/match) vs productive recall (type/build/say)."""

    RECOGNITION = "RECOGNITION"
    RECALL = "RECALL"


class MediaType(StrEnum):
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    SUBTITLE = "SUBTITLE"


class MediaStatus(StrEnum):
    PENDING = "PENDING"
    READY = "READY"
    FAILED = "FAILED"


class EnrollmentStatus(StrEnum):
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class LessonProgressStatus(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
