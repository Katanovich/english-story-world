import logging
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import AppError
from app.core.security import (
    hash_password,
    hash_token,
    new_token,
    password_problem,
    verify_password,
)
from app.models import AuthSession, PasswordResetToken, User
from app.models.enums import AccountStatus

logger = logging.getLogger("app.auth")

RESET_TOKEN_TTL = timedelta(minutes=30)
INVITE_TOKEN_TTL = timedelta(days=7)


def now() -> datetime:
    return datetime.now(UTC)


def find_user_by_login(db: Session, login: str) -> User | None:
    login = login.strip().lower()
    return db.scalar(
        select(User).where(or_(func.lower(User.username) == login, func.lower(User.email) == login))
    )


def authenticate(db: Session, login: str, password: str) -> User:
    user = find_user_by_login(db, login)
    if not verify_password(password, user.password_hash if user else None) or user is None:
        raise AppError(401, "Wrong username or password.", code="invalid_credentials")
    if user.status != AccountStatus.ACTIVE:
        raise AppError(403, "This account is not active.", code="account_inactive")
    return user


def create_session(db: Session, user: User) -> tuple[str, datetime]:
    token = new_token()
    expires_at = now() + timedelta(hours=get_settings().session_ttl_hours)
    db.add(AuthSession(user_id=user.id, token_hash=hash_token(token), expires_at=expires_at))
    user.last_login_at = now()
    db.commit()
    return token, expires_at


def user_for_session_token(db: Session, token: str) -> User | None:
    session = db.scalar(
        select(AuthSession).where(
            AuthSession.token_hash == hash_token(token),
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > now(),
        )
    )
    if session is None:
        return None
    return db.get(User, session.user_id)


def revoke_session(db: Session, token: str) -> None:
    db.execute(
        update(AuthSession)
        .where(AuthSession.token_hash == hash_token(token), AuthSession.revoked_at.is_(None))
        .values(revoked_at=now())
    )
    db.commit()


def revoke_all_sessions(db: Session, user_id: uuid.UUID) -> None:
    """Does not commit: callers commit together with the change that caused it."""
    db.execute(
        update(AuthSession)
        .where(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
        .values(revoked_at=now())
    )


def validate_new_password(password: str) -> None:
    problem = password_problem(password)
    if problem:
        raise AppError(422, problem, code="weak_password")


def set_password(db: Session, user: User, password: str) -> None:
    validate_new_password(password)
    user.password_hash = hash_password(password)
    revoke_all_sessions(db, user.id)


def issue_reset_token(
    db: Session, user: User, ttl: timedelta = RESET_TOKEN_TTL
) -> tuple[str, datetime]:
    """Create a single-use token. Older unused tokens for the user are invalidated."""
    db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None))
        .values(used_at=now())
    )
    token = new_token()
    expires_at = now() + ttl
    db.add(PasswordResetToken(user_id=user.id, token_hash=hash_token(token), expires_at=expires_at))
    return token, expires_at


def request_password_reset(db: Session, login: str) -> None:
    """Always succeeds from the caller's view, so it cannot be used to discover accounts.

    No email service is configured yet. In development the link is written to the server
    log; in production nothing is sent until an email provider is added (see README).
    """
    user = find_user_by_login(db, login)
    if user is None or user.status in (AccountStatus.SUSPENDED, AccountStatus.INACTIVE):
        return
    token, _ = issue_reset_token(db, user)
    db.commit()
    if not get_settings().is_production:
        logger.warning("DEV ONLY password reset token for %s: %s", user.username, token)


def confirm_password_reset(db: Session, token: str, new_password: str) -> None:
    record = db.scalar(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == hash_token(token))
    )
    if record is None or record.used_at is not None or record.expires_at <= now():
        raise AppError(400, "This reset link is invalid or has expired.", code="invalid_token")
    user = db.get(User, record.user_id)
    if user is None or user.status in (AccountStatus.SUSPENDED, AccountStatus.INACTIVE):
        raise AppError(400, "This reset link is invalid or has expired.", code="invalid_token")
    set_password(db, user, new_password)
    record.used_at = now()
    if user.status == AccountStatus.INVITED:
        user.status = AccountStatus.ACTIVE
    db.commit()
