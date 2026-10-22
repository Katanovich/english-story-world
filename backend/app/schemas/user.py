import uuid
from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from app.models.enums import AccountStatus, UserRole
from app.schemas.common import ApiModel, OrmModel

USERNAME_PATTERN = r"^[a-zA-Z0-9_.-]{3,64}$"


class UserPublic(OrmModel):
    """What a user may see about themselves."""

    id: uuid.UUID
    username: str
    email: str | None
    display_name: str
    role: UserRole
    status: AccountStatus


class UserAdminView(UserPublic):
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None
    last_activity_at: datetime | None


class LoginRequest(ApiModel):
    login: str = Field(min_length=1, max_length=254, description="Username or email")
    password: str = Field(min_length=1, max_length=256)


class ChangePasswordRequest(ApiModel):
    current_password: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=1, max_length=256)


class PasswordResetRequest(ApiModel):
    login: str = Field(min_length=1, max_length=254)


class PasswordResetConfirm(ApiModel):
    token: str = Field(min_length=10, max_length=128)
    new_password: str = Field(min_length=1, max_length=256)


class StudentCreate(ApiModel):
    """Admin creates a student. Role is never accepted from the client."""

    username: str = Field(pattern=USERNAME_PATTERN)
    display_name: str = Field(min_length=1, max_length=80)
    email: EmailStr | None = None
    # If omitted, the account is INVITED and a one-time set-password token is returned.
    password: str | None = Field(default=None, max_length=256)

    @field_validator("username")
    @classmethod
    def _lower(cls, v: str) -> str:
        return v.lower()


class StudentUpdate(ApiModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=80)
    email: EmailStr | None = None


class StatusChange(ApiModel):
    status: AccountStatus
    reason: str | None = Field(default=None, max_length=500)


class StudentCreated(OrmModel):
    user: UserAdminView
    # Only present when the account was created without a password (INVITED).
    set_password_token: str | None = None


class ResetTokenIssued(OrmModel):
    token: str
    expires_at: datetime
