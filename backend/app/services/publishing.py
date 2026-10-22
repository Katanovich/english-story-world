"""Checks run before a lesson can be published (also shown live in the CMS)."""

import uuid

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exercises.definitions import DefinitionError, validate_definition
from app.models import Course, Lesson, LessonLearningItem, MediaAsset
from app.models.enums import (
    ExerciseType,
    LessonItemRole,
    LessonSection,
    MediaStatus,
    PublicationStatus,
)
from app.schemas.admin import ValidationReport
from app.schemas.content import LessonContent
from app.services import curriculum


def _media_ok(db: Session, asset_id: uuid.UUID | str | None) -> bool:
    if asset_id is None:
        return True
    asset = db.get(MediaAsset, uuid.UUID(str(asset_id)))
    return asset is not None and asset.status == MediaStatus.READY


def validate_lesson(db: Session, lesson: Lesson) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []

    if not lesson.title.strip():
        errors.append("Нет названия урока.")
    if not lesson.objectives:
        errors.append("Добавьте хотя бы одну учебную цель.")

    track_ids: set[str] = set()
    try:
        content = LessonContent.model_validate(lesson.content)
        track_ids = {t.id for t in content.listening}
        for media_id in content.media_ids():
            if not _media_ok(db, media_id):
                errors.append(f"Контент ссылается на недоступный медиафайл {media_id}.")
        if not content.reading:
            warnings.append("В уроке нет текста для чтения.")
    except ValidationError as exc:
        for e in exc.errors():
            errors.append(f"Контент: {'.'.join(map(str, e['loc']))}: {e['msg']}")

    if not lesson.exercises:
        errors.append("В уроке нет ни одного упражнения.")
    sections = {e.section for e in lesson.exercises}
    if lesson.exercises and LessonSection.QUIZ not in sections:
        warnings.append("Нет итогового теста (раздел QUIZ).")

    for ex in lesson.exercises:
        label = f"Упражнение «{ex.key}»"
        try:
            validate_definition(ex.type, ex.prompt, ex.answer)
        except DefinitionError as exc:
            errors.extend(f"{label}: {msg}" for msg in exc.errors)
        listening_id = ex.prompt.get("listening_id")
        if listening_id and listening_id not in track_ids:
            errors.append(f"{label}: аудиодиалог «{listening_id}» не найден в контенте.")
        for media_id in (ex.image_id, ex.audio_id):
            if not _media_ok(db, media_id):
                errors.append(f"{label}: медиафайл недоступен.")
        if ex.type != ExerciseType.SPEAKING and not ex.item_links:
            warnings.append(
                f"{label}: не связано со словами/грамматикой (не влияет на повторение)."
            )

    roles = set(
        db.scalars(select(LessonLearningItem.role).where(LessonLearningItem.lesson_id == lesson.id))
    )
    if LessonItemRole.NEW not in roles:
        warnings.append("В уроке нет нового материала (NEW).")
    if lesson.position > 1 and not roles & {
        LessonItemRole.RECENT_REVIEW,
        LessonItemRole.OLDER_REVIEW,
    }:
        warnings.append("Урок не повторяет ранее изученный материал.")

    for ep in lesson.episodes:
        if not ep.video_asset_id and ep.status == PublicationStatus.PUBLISHED:
            warnings.append(f"Эпизод «{ep.title}» пока без видео (ученики увидят заглушку).")
        for media_id in (ep.video_asset_id, ep.subtitle_asset_id, ep.poster_image_id):
            if not _media_ok(db, media_id):
                errors.append(f"Эпизод «{ep.title}»: медиафайл недоступен.")

    course: Course = curriculum.course_of_lesson(db, lesson)
    if course.status != PublicationStatus.PUBLISHED:
        warnings.append("Курс не опубликован — ученики не увидят урок.")
    return ValidationReport(errors=errors, warnings=warnings)
