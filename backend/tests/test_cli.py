import pytest
from sqlalchemy import select

from app.cli import CommandError, create_admin
from app.models import User
from app.models.enums import UserRole


def test_create_admin_is_idempotent(db):
    assert "created" in create_admin("Admin@Example.com", "Admin", "Strong-admin-pass-1")
    assert "already exists" in create_admin("admin@example.com", "admin", "Strong-admin-pass-1")
    admins = db.scalars(select(User).where(User.role == UserRole.ADMIN)).all()
    assert len(admins) == 1
    assert admins[0].email == "admin@example.com"


@pytest.mark.parametrize("password", [None, "", "short1!", "password123", "abcdefghijklmnop"])
def test_create_admin_rejects_missing_or_weak_password(password):
    with pytest.raises(CommandError):
        create_admin("a@example.com", "admin", password)


def test_create_admin_refuses_to_promote_existing_student(make_user):
    make_user("admin")
    with pytest.raises(CommandError):
        create_admin(None, "admin", "Strong-admin-pass-1")
