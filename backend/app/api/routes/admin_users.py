import uuid

from fastapi import APIRouter, Query, status
from sqlalchemy import func, or_, select

from app.api.deps import AdminUser, DbSession
from app.core.errors import AppError
from app.core.security import hash_password, new_token
from app.models import User
from app.models.enums import AccountStatus, UserRole
from app.schemas.common import Page
from app.schemas.user import (
    ResetTokenIssued,
    StatusChange,
    StudentCreate,
    StudentCreated,
    StudentUpdate,
    UserAdminView,
)
from app.services import audit
from app.services import auth as auth_service

router = APIRouter(prefix="/admin/students", tags=["admin: students"])


def _get_student(db: DbSession, student_id: uuid.UUID) -> User:
    user = db.get(User, student_id)
    if user is None or user.role != UserRole.STUDENT:
        raise AppError(404, "Student not found.")
    return user


@router.get("", response_model=Page[UserAdminView])
def list_students(
    db: DbSession,
    _: AdminUser,
    q: str | None = Query(default=None, max_length=100, description="Search name/username/email"),
    status_filter: AccountStatus | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    stmt = select(User).where(User.role == UserRole.STUDENT)
    if q:
        pattern = f"%{q.strip().lower()}%"
        stmt = stmt.where(
            or_(
                func.lower(User.username).like(pattern),
                func.lower(User.display_name).like(pattern),
                func.lower(User.email).like(pattern),
            )
        )
    if status_filter:
        stmt = stmt.where(User.status == status_filter)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(User.created_at.desc(), User.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=StudentCreated, status_code=status.HTTP_201_CREATED)
def create_student(body: StudentCreate, db: DbSession, admin: AdminUser):
    if auth_service.find_user_by_login(db, body.username) or (
        body.email and auth_service.find_user_by_login(db, body.email)
    ):
        raise AppError(409, "A user with this username or email already exists.")
    if body.password:
        auth_service.validate_new_password(body.password)
        password_hash, initial_status = hash_password(body.password), AccountStatus.ACTIVE
    else:
        # Unusable random password until the student sets one with the invite token.
        password_hash, initial_status = hash_password(new_token()), AccountStatus.INVITED
    user = User(
        username=body.username,
        email=str(body.email).lower() if body.email else None,
        display_name=body.display_name,
        password_hash=password_hash,
        role=UserRole.STUDENT,
        status=initial_status,
    )
    db.add(user)
    db.flush()
    token = None
    if initial_status == AccountStatus.INVITED:
        token, _ = auth_service.issue_reset_token(db, user, ttl=auth_service.INVITE_TOKEN_TTL)
    audit.record(db, admin.id, "student.create", "user", user.id, {"status": initial_status})
    db.commit()
    db.refresh(user)
    return StudentCreated(user=UserAdminView.model_validate(user), set_password_token=token)


@router.get("/{student_id}", response_model=UserAdminView)
def get_student(student_id: uuid.UUID, db: DbSession, _: AdminUser):
    return _get_student(db, student_id)


@router.patch("/{student_id}", response_model=UserAdminView)
def update_student(student_id: uuid.UUID, body: StudentUpdate, db: DbSession, admin: AdminUser):
    user = _get_student(db, student_id)
    changes = body.model_dump(exclude_unset=True)
    if "email" in changes and changes["email"]:
        changes["email"] = str(changes["email"]).lower()
        existing = auth_service.find_user_by_login(db, changes["email"])
        if existing and existing.id != user.id:
            raise AppError(409, "This email is already used.")
    for field, value in changes.items():
        setattr(user, field, value)
    audit.record(db, admin.id, "student.update", "user", user.id, {"fields": sorted(changes)})
    db.commit()
    db.refresh(user)
    return user


@router.post("/{student_id}/status", response_model=UserAdminView)
def change_status(student_id: uuid.UUID, body: StatusChange, db: DbSession, admin: AdminUser):
    """Activate, suspend or deactivate. Learning history is never deleted."""
    user = _get_student(db, student_id)
    previous = user.status
    if body.status == AccountStatus.INVITED:
        raise AppError(422, "Use the password-reset endpoint to re-invite a student.")
    user.status = body.status
    if body.status != AccountStatus.ACTIVE:
        auth_service.revoke_all_sessions(db, user.id)
    audit.record(
        db,
        admin.id,
        "student.status_change",
        "user",
        user.id,
        {"from": previous, "to": body.status, "reason": body.reason},
    )
    db.commit()
    db.refresh(user)
    return user


@router.post("/{student_id}/password-reset", response_model=ResetTokenIssued)
def issue_password_reset(student_id: uuid.UUID, db: DbSession, admin: AdminUser):
    """Children often have no email: the admin receives a one-time token to hand over."""
    user = _get_student(db, student_id)
    if user.status in (AccountStatus.SUSPENDED, AccountStatus.INACTIVE):
        raise AppError(409, "Reactivate the account before resetting its password.")
    token, expires_at = auth_service.issue_reset_token(db, user)
    audit.record(db, admin.id, "student.password_reset_issued", "user", user.id)
    db.commit()
    return ResetTokenIssued(token=token, expires_at=expires_at)
