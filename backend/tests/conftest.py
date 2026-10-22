"""Test setup: runs every test against a dedicated PostgreSQL test database.

The test database is (re)created once per session and migrated with Alembic, so the
tests also verify that migrations produce a working schema.
"""

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.core.config import get_settings

_settings = get_settings()
TEST_DB_URL = _settings.test_database_url or f"{_settings.database_url}_test"
# Must happen before app.db.session is imported anywhere.
os.environ["DATABASE_URL"] = TEST_DB_URL
os.environ["LOCAL_STORAGE_DIR"] = tempfile.mkdtemp(prefix="esw-test-media-")
get_settings.cache_clear()

BACKEND_DIR = Path(__file__).resolve().parents[1]


def _recreate_database(url: str) -> None:
    target = make_url(url)
    admin_engine = create_engine(target.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{target.database}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{target.database}"'))
    admin_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> Iterator[None]:
    from alembic import command
    from alembic.config import Config

    _recreate_database(TEST_DB_URL)
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.attributes["database_url"] = TEST_DB_URL
    command.upgrade(cfg, "head")
    yield


@pytest.fixture
def client() -> Iterator["TestClient"]:  # noqa: F821
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clean_tables() -> Iterator[None]:
    """Each test starts with empty tables (schema stays migrated)."""
    yield
    from app.db.session import engine
    from app.models import Base
    from app.services.rate_limit import login_limiter

    names = ", ".join(f'"{t.name}"' for t in Base.metadata.sorted_tables)
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE {names} RESTART IDENTITY CASCADE"))
    login_limiter.reset()


@pytest.fixture
def db():
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        yield session


PASSWORD = "Secret-pass-123"


@pytest.fixture
def make_user(db):
    from app.core.security import hash_password
    from app.models import User
    from app.models.enums import AccountStatus, UserRole

    def _make(
        username: str = "student1",
        role: UserRole = UserRole.STUDENT,
        status: AccountStatus = AccountStatus.ACTIVE,
        password: str = PASSWORD,
        email: str | None = None,
    ) -> User:
        user = User(
            username=username,
            email=email,
            display_name=username.title(),
            password_hash=hash_password(password),
            role=role,
            status=status,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    return _make


@pytest.fixture
def new_client():
    """Factory for independent clients (separate cookie jars = separate browsers)."""
    from fastapi.testclient import TestClient

    from app.main import app

    clients = []

    def _new() -> TestClient:
        c = TestClient(app)
        clients.append(c)
        return c

    yield _new
    for c in clients:
        c.close()


@pytest.fixture
def login_as(new_client, make_user):
    """Create a user and return a client logged in as that user."""
    from app.models.enums import UserRole

    def _login(username: str = "student1", role: UserRole = UserRole.STUDENT, **kw):
        user = make_user(username=username, role=role, **kw)
        c = new_client()
        r = c.post("/api/v1/auth/login", json={"login": username, "password": PASSWORD})
        assert r.status_code == 200, r.text
        return c, user

    return _login
