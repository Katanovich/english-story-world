from fastapi import APIRouter, Request, Response, status

from app.api.deps import CurrentUser, DbSession, session_token
from app.core.config import get_settings
from app.core.errors import AppError
from app.core.security import verify_password
from app.schemas.common import Message
from app.schemas.user import (
    ChangePasswordRequest,
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    UserPublic,
)
from app.services import auth as auth_service
from app.services.rate_limit import login_limiter

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_session_cookie(response: Response, token: str, max_age: int) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=max_age,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        path="/",
    )


@router.post("/login", response_model=UserPublic)
def login(body: LoginRequest, request: Request, response: Response, db: DbSession):
    client_ip = request.client.host if request.client else "unknown"
    limiter_key = f"{client_ip}:{body.login.lower()}"
    if login_limiter.is_blocked(limiter_key):
        raise AppError(429, "Too many attempts. Please wait a few minutes and try again.")
    try:
        user = auth_service.authenticate(db, body.login, body.password)
    except AppError:
        login_limiter.record_failure(limiter_key)
        raise
    login_limiter.reset(limiter_key)
    token, _ = auth_service.create_session(db, user)
    _set_session_cookie(response, token, get_settings().session_ttl_hours * 3600)
    return user


@router.post("/logout", response_model=Message)
def logout(request: Request, response: Response, db: DbSession):
    token = session_token(request)
    if token:
        auth_service.revoke_session(db, token)
    response.delete_cookie(get_settings().session_cookie_name, path="/")
    return Message(message="Logged out.")


@router.get("/me", response_model=UserPublic)
def me(user: CurrentUser):
    return user


@router.post("/change-password", response_model=Message)
def change_password(
    body: ChangePasswordRequest, user: CurrentUser, response: Response, db: DbSession
):
    if not verify_password(body.current_password, user.password_hash):
        raise AppError(400, "Current password is wrong.", code="invalid_credentials")
    auth_service.set_password(db, user, body.new_password)  # revokes all sessions
    db.commit()
    response.delete_cookie(get_settings().session_cookie_name, path="/")
    return Message(message="Password changed. Please log in again.")


@router.post(
    "/password-reset/request", response_model=Message, status_code=status.HTTP_202_ACCEPTED
)
def password_reset_request(body: PasswordResetRequest, db: DbSession):
    auth_service.request_password_reset(db, body.login)
    return Message(message="If this account exists, reset instructions have been sent.")


@router.post("/password-reset/confirm", response_model=Message)
def password_reset_confirm(body: PasswordResetConfirm, db: DbSession):
    auth_service.confirm_password_reset(db, body.token, body.new_password)
    return Message(message="Password updated. You can log in now.")
