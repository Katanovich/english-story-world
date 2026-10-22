from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import AppError
from app.db.session import get_db
from app.models import User
from app.models.enums import AccountStatus, UserRole
from app.services.auth import user_for_session_token

DbSession = Annotated[Session, Depends(get_db)]

_ACTIVITY_WRITE_INTERVAL = timedelta(minutes=5)


def session_token(request: Request) -> str | None:
    return request.cookies.get(get_settings().session_cookie_name)


def get_current_user(request: Request, db: DbSession) -> User:
    token = session_token(request)
    user = user_for_session_token(db, token) if token else None
    if user is None:
        raise AppError(401, "Please log in.", code="not_authenticated")
    # Status is checked on every request, so suspension takes effect immediately.
    if user.status != AccountStatus.ACTIVE:
        raise AppError(403, "This account is not active.", code="account_inactive")
    now = datetime.now(UTC)
    if user.last_activity_at is None or now - user.last_activity_at > _ACTIVITY_WRITE_INTERVAL:
        user.last_activity_at = now
        db.commit()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> User:
    if user.role != UserRole.ADMIN:
        raise AppError(403, "Administrator access required.")
    return user


def require_student(user: CurrentUser) -> User:
    if user.role != UserRole.STUDENT:
        raise AppError(403, "Student access required.")
    return user


AdminUser = Annotated[User, Depends(require_admin)]
StudentUser = Annotated[User, Depends(require_student)]
