"""Admin CMS: curriculum structure, lessons, exercises, learning items, episodes, audit."""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Query, status
from pydantic import ValidationError
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.api.deps import AdminUser, DbSession
from app.api.routes.media import _require_asset
from app.core.errors import AppError
from app.exercises.definitions import DefinitionError, validate_definition
from app.models import (
    AuditLog,
    Course,
    CourseLevel,
    Exercise,
    ExerciseAttempt,
    ExerciseLearningItem,
    LearningItem,
    Lesson,
    LessonLearningItem,
    MediaAsset,
    StoryEpisode,
    Unit,
    User,
)
from app.models.enums import (
    AccountStatus,
    ExerciseType,
    MediaType,
    PublicationStatus,
    UserRole,
)
from app.schemas.admin import (
    AuditEntry,
    CourseIn,
    CourseNode,
    CourseUpdate,
    EpisodeAdmin,
    EpisodeIn,
    EpisodeUpdate,
    ExerciseAdmin,
    ExerciseIn,
    ExerciseUpdate,
    ItemLink,
    LearningItemAdmin,
    LearningItemIn,
    LearningItemUpdate,
    LessonAdmin,
    LessonIn,
    LessonNode,
    LessonUpdate,
    LevelIn,
    LevelNode,
    LevelUpdate,
    Overview,
    UnitIn,
    UnitNode,
    UnitUpdate,
    ValidationReport,
)
from app.schemas.common import Page
from app.schemas.content import LessonContent
from app.services import audit, curriculum
from app.services.publishing import validate_lesson

router = APIRouter(prefix="/admin", tags=["admin: content"])


def _get(db, model, obj_id: uuid.UUID, name: str):
    obj = db.get(model, obj_id)
    if obj is None:
        raise AppError(404, f"{name} not found.")
    return obj


def _flush(db, conflict_message: str = "A record with this slug or key already exists.") -> None:
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise AppError(409, conflict_message) from exc


def _commit(db, conflict_message: str = "A record with this slug or key already exists.") -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AppError(409, conflict_message) from exc


# ---- Overview & audit -----------------------------------------------------------------


@router.get("/overview", response_model=Overview)
def overview(db: DbSession, _: AdminUser):
    by_status = dict(
        db.execute(
            select(User.status, func.count())
            .where(User.role == UserRole.STUDENT)
            .group_by(User.status)
        ).all()
    )
    since = datetime.now(UTC) - timedelta(days=7)
    count = lambda stmt: db.scalar(stmt) or 0  # noqa: E731
    return Overview(
        students_by_status={s: by_status.get(s, 0) for s in AccountStatus},
        lessons_published=count(
            select(func.count()).where(Lesson.status == PublicationStatus.PUBLISHED)
        ),
        lessons_draft=count(select(func.count()).where(Lesson.status == PublicationStatus.DRAFT)),
        learning_items=count(select(func.count()).select_from(LearningItem)),
        media_assets=count(select(func.count()).select_from(MediaAsset)),
        attempts_last_7_days=count(select(func.count()).where(ExerciseAttempt.created_at >= since)),
        active_students_last_7_days=count(
            select(func.count(func.distinct(ExerciseAttempt.user_id))).where(
                ExerciseAttempt.created_at >= since
            )
        ),
    )


@router.get("/audit-logs", response_model=Page[AuditEntry])
def audit_logs(
    db: DbSession,
    _: AdminUser,
    action: str | None = Query(default=None, max_length=64),
    entity_id: str | None = Query(default=None, max_length=64),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    stmt = select(AuditLog, User.username).outerjoin(User, User.id == AuditLog.actor_id)
    if action:
        stmt = stmt.where(AuditLog.action.like(f"{action}%"))
    if entity_id:
        stmt = stmt.where(AuditLog.entity_id == entity_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.execute(
        stmt.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [
        AuditEntry.model_validate(log).model_copy(update={"actor_username": username})
        for log, username in rows
    ]
    return Page(items=items, total=total, page=page, page_size=page_size)


# ---- Course structure -----------------------------------------------------------------


@router.get("/courses", response_model=list[CourseNode])
def course_tree(db: DbSession, _: AdminUser):
    courses = db.scalars(
        select(Course)
        .order_by(Course.title)
        .options(
            selectinload(Course.levels)
            .selectinload(CourseLevel.units)
            .selectinload(Unit.lessons)
            .selectinload(Lesson.exercises)
        )
    ).all()
    return [
        CourseNode(
            id=c.id,
            slug=c.slug,
            title=c.title,
            description=c.description,
            status=c.status,
            levels=[
                LevelNode(
                    id=lv.id,
                    cefr_level=lv.cefr_level,
                    title=lv.title,
                    description=lv.description,
                    position=lv.position,
                    units=[
                        UnitNode(
                            id=u.id,
                            slug=u.slug,
                            title=u.title,
                            description=u.description,
                            position=u.position,
                            lessons=[
                                LessonNode(
                                    id=ls.id,
                                    slug=ls.slug,
                                    title=ls.title,
                                    status=ls.status,
                                    position=ls.position,
                                    content_version=ls.content_version,
                                    exercise_count=len(ls.exercises),
                                )
                                for ls in u.lessons
                            ],
                        )
                        for u in lv.units
                    ],
                )
                for lv in c.levels
            ],
        )
        for c in courses
    ]


@router.post("/courses", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_course(body: CourseIn, db: DbSession, admin: AdminUser):
    course = Course(**body.model_dump(), status=PublicationStatus.DRAFT)
    db.add(course)
    _flush(db)
    audit.record(db, admin.id, "course.create", "course", course.id, {"slug": body.slug})
    _commit(db)
    return {"id": str(course.id)}


@router.patch("/courses/{course_id}", response_model=dict)
def update_course(course_id: uuid.UUID, body: CourseUpdate, db: DbSession, admin: AdminUser):
    course = _get(db, Course, course_id, "Course")
    changes = body.model_dump(exclude_unset=True)
    for k, v in changes.items():
        setattr(course, k, v)
    audit.record(db, admin.id, "course.update", "course", course.id, {"fields": sorted(changes)})
    _commit(db)
    return {"id": str(course.id)}


@router.post(
    "/courses/{course_id}/levels", status_code=status.HTTP_201_CREATED, response_model=dict
)
def create_level(course_id: uuid.UUID, body: LevelIn, db: DbSession, admin: AdminUser):
    _get(db, Course, course_id, "Course")
    level = CourseLevel(course_id=course_id, **body.model_dump())
    db.add(level)
    _flush(db)
    audit.record(db, admin.id, "level.create", "course_level", level.id, {"cefr": body.cefr_level})
    _commit(db, "This course already has this CEFR level.")
    return {"id": str(level.id)}


@router.patch("/levels/{level_id}", response_model=dict)
def update_level(level_id: uuid.UUID, body: LevelUpdate, db: DbSession, admin: AdminUser):
    level = _get(db, CourseLevel, level_id, "Level")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(level, k, v)
    audit.record(db, admin.id, "level.update", "course_level", level.id)
    _commit(db)
    return {"id": str(level.id)}


@router.post("/levels/{level_id}/units", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_unit(level_id: uuid.UUID, body: UnitIn, db: DbSession, admin: AdminUser):
    _get(db, CourseLevel, level_id, "Level")
    unit = Unit(level_id=level_id, **body.model_dump())
    db.add(unit)
    _flush(db)
    audit.record(db, admin.id, "unit.create", "unit", unit.id, {"slug": body.slug})
    _commit(db)
    return {"id": str(unit.id)}


@router.patch("/units/{unit_id}", response_model=dict)
def update_unit(unit_id: uuid.UUID, body: UnitUpdate, db: DbSession, admin: AdminUser):
    unit = _get(db, Unit, unit_id, "Unit")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(unit, k, v)
    audit.record(db, admin.id, "unit.update", "unit", unit.id)
    _commit(db)
    return {"id": str(unit.id)}


# ---- Lessons --------------------------------------------------------------------------


def _exercise_admin(db, ex: Exercise) -> ExerciseAdmin:
    out = ExerciseAdmin.model_validate(ex)
    out.learning_item_ids = [link.learning_item_id for link in ex.item_links]
    out.attempt_count = (
        db.scalar(select(func.count()).where(ExerciseAttempt.exercise_id == ex.id)) or 0
    )
    return out


def _lesson_admin(db, lesson: Lesson) -> LessonAdmin:
    course = curriculum.course_of_lesson(db, lesson)
    links = db.scalars(
        select(LessonLearningItem).where(LessonLearningItem.lesson_id == lesson.id)
    ).all()
    return LessonAdmin(
        id=lesson.id,
        unit_id=lesson.unit_id,
        course_id=course.id,
        slug=lesson.slug,
        title=lesson.title,
        description=lesson.description,
        objectives=lesson.objectives,
        cefr_level=lesson.cefr_level,
        position=lesson.position,
        estimated_minutes=lesson.estimated_minutes,
        content=lesson.content,
        status=lesson.status,
        content_version=lesson.content_version,
        cover_image_id=lesson.cover_image_id,
        updated_at=lesson.updated_at,
        items=[ItemLink(learning_item_id=li.learning_item_id, role=li.role) for li in links],
        exercises=[_exercise_admin(db, e) for e in lesson.exercises],
        episodes=[EpisodeAdmin.model_validate(ep) for ep in lesson.episodes],
    )


def _bump_if_published(lesson: Lesson) -> None:
    """Editing a live lesson creates a new content version (old attempts keep theirs)."""
    if lesson.status == PublicationStatus.PUBLISHED:
        lesson.content_version += 1


@router.post(
    "/units/{unit_id}/lessons", status_code=status.HTTP_201_CREATED, response_model=LessonAdmin
)
def create_lesson(unit_id: uuid.UUID, body: LessonIn, db: DbSession, admin: AdminUser):
    unit = _get(db, Unit, unit_id, "Unit")
    level = db.get(CourseLevel, unit.level_id)
    lesson = Lesson(
        unit_id=unit.id,
        cefr_level=level.cefr_level,
        status=PublicationStatus.DRAFT,
        content={},
        objectives=[],
        **body.model_dump(),
    )
    db.add(lesson)
    _flush(db)
    audit.record(db, admin.id, "lesson.create", "lesson", lesson.id, {"slug": body.slug})
    _commit(db)
    db.refresh(lesson)
    return _lesson_admin(db, lesson)


@router.get("/lessons/{lesson_id}", response_model=LessonAdmin)
def get_lesson(lesson_id: uuid.UUID, db: DbSession, _: AdminUser):
    return _lesson_admin(db, _get(db, Lesson, lesson_id, "Lesson"))


@router.patch("/lessons/{lesson_id}", response_model=LessonAdmin)
def update_lesson(lesson_id: uuid.UUID, body: LessonUpdate, db: DbSession, admin: AdminUser):
    lesson = _get(db, Lesson, lesson_id, "Lesson")
    changes = body.model_dump(exclude_unset=True)
    if "content" in changes:
        try:
            changes["content"] = LessonContent.model_validate(changes["content"]).model_dump(
                mode="json", exclude_none=True
            )
        except ValidationError as exc:
            raise AppError(
                422,
                "Контент урока заполнен неверно.",
                details=[f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()],
            ) from exc
    if "cover_image_id" in changes:
        _require_asset(db, changes["cover_image_id"], MediaType.IMAGE)
    if "objectives" in changes:
        changes["objectives"] = [o.strip() for o in changes["objectives"] if o.strip()]
    changed = [k for k, v in changes.items() if getattr(lesson, k) != v]
    for k in changed:
        setattr(lesson, k, changes[k])
    if set(changed) & {"content", "objectives", "title"}:
        _bump_if_published(lesson)
    audit.record(db, admin.id, "lesson.update", "lesson", lesson.id, {"fields": sorted(changed)})
    _commit(db)
    db.refresh(lesson)
    return _lesson_admin(db, lesson)


@router.get("/lessons/{lesson_id}/validation", response_model=ValidationReport)
def lesson_validation(lesson_id: uuid.UUID, db: DbSession, _: AdminUser):
    return validate_lesson(db, _get(db, Lesson, lesson_id, "Lesson"))


@router.post("/lessons/{lesson_id}/publish", response_model=LessonAdmin)
def publish_lesson(lesson_id: uuid.UUID, db: DbSession, admin: AdminUser):
    lesson = _get(db, Lesson, lesson_id, "Lesson")
    report = validate_lesson(db, lesson)
    if report.errors:
        raise AppError(422, "Урок нельзя опубликовать: есть ошибки.", details=report.errors)
    if lesson.status != PublicationStatus.PUBLISHED:
        lesson.status = PublicationStatus.PUBLISHED
        audit.record(
            db,
            admin.id,
            "lesson.publish",
            "lesson",
            lesson.id,
            {"content_version": lesson.content_version, "warnings": report.warnings},
        )
        _commit(db)
    db.refresh(lesson)
    return _lesson_admin(db, lesson)


@router.post("/lessons/{lesson_id}/unpublish", response_model=LessonAdmin)
def unpublish_lesson(lesson_id: uuid.UUID, db: DbSession, admin: AdminUser):
    """Hides the lesson from students. Their progress and attempts are kept."""
    lesson = _get(db, Lesson, lesson_id, "Lesson")
    if lesson.status != PublicationStatus.DRAFT:
        lesson.status = PublicationStatus.DRAFT
        audit.record(db, admin.id, "lesson.unpublish", "lesson", lesson.id)
        _commit(db)
    db.refresh(lesson)
    return _lesson_admin(db, lesson)


@router.put("/lessons/{lesson_id}/items", response_model=LessonAdmin)
def set_lesson_items(lesson_id: uuid.UUID, body: list[ItemLink], db: DbSession, admin: AdminUser):
    lesson = _get(db, Lesson, lesson_id, "Lesson")
    wanted = {link.learning_item_id: link.role for link in body}
    found = set(db.scalars(select(LearningItem.id).where(LearningItem.id.in_(wanted))))
    if missing := set(wanted) - found:
        raise AppError(422, f"Unknown learning items: {', '.join(map(str, missing))}")
    existing = {
        li.learning_item_id: li
        for li in db.scalars(
            select(LessonLearningItem).where(LessonLearningItem.lesson_id == lesson.id)
        )
    }
    for item_id, link in existing.items():
        if item_id not in wanted:
            db.delete(link)
        else:
            link.role = wanted[item_id]
    for item_id, role in wanted.items():
        if item_id not in existing:
            db.add(LessonLearningItem(lesson_id=lesson.id, learning_item_id=item_id, role=role))
    audit.record(db, admin.id, "lesson.items_set", "lesson", lesson.id, {"count": len(wanted)})
    _commit(db)
    return _lesson_admin(db, lesson)


# ---- Exercises ------------------------------------------------------------------------


def _validated(ex_type: ExerciseType, prompt: dict, answer: dict) -> tuple[dict, dict]:
    try:
        return validate_definition(ex_type, prompt, answer)
    except DefinitionError as exc:
        raise AppError(422, "Упражнение заполнено неверно.", details=exc.errors) from exc


def _set_exercise_items(db, exercise: Exercise, item_ids: list[uuid.UUID]) -> None:
    found = set(db.scalars(select(LearningItem.id).where(LearningItem.id.in_(item_ids))))
    if missing := set(item_ids) - found:
        raise AppError(422, f"Unknown learning items: {', '.join(map(str, missing))}")
    current = {link.learning_item_id: link for link in exercise.item_links}
    for item_id, link in current.items():
        if item_id not in found:
            db.delete(link)
    for item_id in found - set(current):
        db.add(ExerciseLearningItem(exercise_id=exercise.id, learning_item_id=item_id))


@router.post(
    "/lessons/{lesson_id}/exercises",
    status_code=status.HTTP_201_CREATED,
    response_model=ExerciseAdmin,
)
def create_exercise(lesson_id: uuid.UUID, body: ExerciseIn, db: DbSession, admin: AdminUser):
    lesson = _get(db, Lesson, lesson_id, "Lesson")
    prompt, answer = _validated(body.type, body.prompt, body.answer)
    _require_asset(db, body.image_id, MediaType.IMAGE)
    _require_asset(db, body.audio_id, MediaType.AUDIO)
    data = body.model_dump(exclude={"prompt", "answer", "learning_item_ids"})
    exercise = Exercise(
        lesson_id=lesson.id,
        prompt=prompt,
        answer=answer,
        is_scored=body.type != ExerciseType.SPEAKING,
        version=1,
        **data,
    )
    db.add(exercise)
    _flush(db)
    _set_exercise_items(db, exercise, body.learning_item_ids)
    _bump_if_published(lesson)
    audit.record(db, admin.id, "exercise.create", "exercise", exercise.id, {"key": body.key})
    _commit(db)
    db.refresh(exercise)
    return _exercise_admin(db, exercise)


@router.patch("/exercises/{exercise_id}", response_model=ExerciseAdmin)
def update_exercise(exercise_id: uuid.UUID, body: ExerciseUpdate, db: DbSession, admin: AdminUser):
    exercise = _get(db, Exercise, exercise_id, "Exercise")
    changes = body.model_dump(exclude_unset=True)
    item_ids = changes.pop("learning_item_ids", None)
    ex_type = changes.get("type", exercise.type)
    if {"type", "prompt", "answer"} & set(changes):
        changes["prompt"], changes["answer"] = _validated(
            ex_type, changes.get("prompt", exercise.prompt), changes.get("answer", exercise.answer)
        )
        changes["is_scored"] = ex_type != ExerciseType.SPEAKING
    if "image_id" in changes:
        _require_asset(db, changes["image_id"], MediaType.IMAGE)
    if "audio_id" in changes:
        _require_asset(db, changes["audio_id"], MediaType.AUDIO)
    changed = [k for k, v in changes.items() if getattr(exercise, k) != v]
    for k in changed:
        setattr(exercise, k, changes[k])
    # Scoring-relevant change => new version, so earlier attempts stay interpretable.
    if set(changed) & {"type", "prompt", "answer", "points"}:
        exercise.version += 1
        _bump_if_published(exercise.lesson)
    if item_ids is not None:
        _set_exercise_items(db, exercise, item_ids)
    audit.record(
        db,
        admin.id,
        "exercise.update",
        "exercise",
        exercise.id,
        {"fields": sorted(changed), "version": exercise.version},
    )
    _commit(db)
    db.refresh(exercise)
    return _exercise_admin(db, exercise)


@router.delete("/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: uuid.UUID, db: DbSession, admin: AdminUser):
    """Only exercises nobody has answered can be deleted; learning history is never removed."""
    exercise = _get(db, Exercise, exercise_id, "Exercise")
    if db.scalar(
        select(ExerciseAttempt.id).where(ExerciseAttempt.exercise_id == exercise.id).limit(1)
    ):
        raise AppError(
            409,
            "У упражнения есть ответы учеников. Его нельзя удалить — измените его вместо этого.",
        )
    lesson = exercise.lesson
    audit.record(db, admin.id, "exercise.delete", "exercise", exercise.id, {"key": exercise.key})
    db.delete(exercise)
    _bump_if_published(lesson)
    _commit(db)


# ---- Episodes -------------------------------------------------------------------------


@router.post(
    "/lessons/{lesson_id}/episodes",
    status_code=status.HTTP_201_CREATED,
    response_model=EpisodeAdmin,
)
def create_episode(lesson_id: uuid.UUID, body: EpisodeIn, db: DbSession, admin: AdminUser):
    _get(db, Lesson, lesson_id, "Lesson")
    episode = StoryEpisode(lesson_id=lesson_id, status=PublicationStatus.DRAFT, **body.model_dump())
    db.add(episode)
    _flush(db)
    audit.record(db, admin.id, "episode.create", "story_episode", episode.id)
    _commit(db, "An episode with this position already exists in the lesson.")
    return episode


@router.patch("/episodes/{episode_id}", response_model=EpisodeAdmin)
def update_episode(episode_id: uuid.UUID, body: EpisodeUpdate, db: DbSession, admin: AdminUser):
    episode = _get(db, StoryEpisode, episode_id, "Episode")
    changes = body.model_dump(exclude_unset=True)
    for k, v in changes.items():
        setattr(episode, k, v)
    audit.record(
        db, admin.id, "episode.update", "story_episode", episode.id, {"fields": sorted(changes)}
    )
    _commit(db, "An episode with this position already exists in the lesson.")
    return episode


# ---- Learning items -------------------------------------------------------------------


@router.get("/learning-items", response_model=Page[LearningItemAdmin])
def list_items(
    db: DbSession,
    _: AdminUser,
    q: str | None = Query(default=None, max_length=100),
    kind: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
):
    stmt = select(LearningItem)
    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(
            or_(
                func.lower(LearningItem.text).like(pattern),
                func.lower(LearningItem.key).like(pattern),
                func.lower(LearningItem.translation_ru).like(pattern),
            )
        )
    if kind:
        stmt = stmt.where(LearningItem.kind == kind)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(LearningItem.key).offset((page - 1) * page_size).limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)


@router.post(
    "/learning-items", status_code=status.HTTP_201_CREATED, response_model=LearningItemAdmin
)
def create_item(body: LearningItemIn, db: DbSession, admin: AdminUser):
    _require_asset(db, body.image_id, MediaType.IMAGE)
    _require_asset(db, body.audio_id, MediaType.AUDIO)
    item = LearningItem(**body.model_dump())
    db.add(item)
    _flush(db)
    audit.record(db, admin.id, "learning_item.create", "learning_item", item.id, {"key": body.key})
    _commit(db, "A learning item with this key already exists.")
    db.refresh(item)
    return item


@router.patch("/learning-items/{item_id}", response_model=LearningItemAdmin)
def update_item(item_id: uuid.UUID, body: LearningItemUpdate, db: DbSession, admin: AdminUser):
    item = _get(db, LearningItem, item_id, "Learning item")
    changes = body.model_dump(exclude_unset=True)
    if "image_id" in changes:
        _require_asset(db, changes["image_id"], MediaType.IMAGE)
    if "audio_id" in changes:
        _require_asset(db, changes["audio_id"], MediaType.AUDIO)
    for k, v in changes.items():
        setattr(item, k, v)
    audit.record(
        db, admin.id, "learning_item.update", "learning_item", item.id, {"fields": sorted(changes)}
    )
    _commit(db)
    db.refresh(item)
    return item
