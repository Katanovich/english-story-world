from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.security import hash_token
from app.models import AuthSession, PasswordResetToken, User
from app.models.enums import AccountStatus, UserRole
from tests.conftest import PASSWORD

LOGIN = "/api/v1/auth/login"
ME = "/api/v1/auth/me"


def test_login_with_username_and_email_sets_httponly_cookie(client, make_user):
    make_user("alex", email="alex@example.com")
    r = client.post(LOGIN, json={"login": "ALEX", "password": PASSWORD})
    assert r.status_code == 200
    assert r.json()["username"] == "alex"
    set_cookie = r.headers["set-cookie"].lower()
    assert "httponly" in set_cookie and "samesite=lax" in set_cookie
    assert "password" not in r.text

    client.cookies.clear()
    r = client.post(LOGIN, json={"login": "alex@example.com", "password": PASSWORD})
    assert r.status_code == 200
    assert client.get(ME).json()["username"] == "alex"


def test_wrong_password_and_unknown_user_give_same_error(client, make_user):
    make_user("alex")
    wrong = client.post(LOGIN, json={"login": "alex", "password": "nope-nope-1"})
    unknown = client.post(LOGIN, json={"login": "ghost", "password": "nope-nope-1"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_passwords_are_hashed_with_argon2(db, make_user):
    user = make_user("alex")
    assert user.password_hash != PASSWORD
    assert user.password_hash.startswith("$argon2id$")


def test_session_token_stored_only_as_hash(client, db, make_user):
    make_user("alex")
    client.post(LOGIN, json={"login": "alex", "password": PASSWORD})
    token = client.cookies.get("esw_session")
    stored = db.scalars(select(AuthSession)).one()
    assert stored.token_hash == hash_token(token) and stored.token_hash != token


def test_unauthenticated_requests_are_rejected(client):
    assert client.get(ME).status_code == 401
    assert client.get("/api/v1/admin/students").status_code == 401
    client.cookies.set("esw_session", "forged-token-value")
    r = client.get(ME)
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "not_authenticated"


def test_logout_revokes_session(client, make_user):
    make_user("alex")
    client.post(LOGIN, json={"login": "alex", "password": PASSWORD})
    token = client.cookies.get("esw_session")
    assert client.post("/api/v1/auth/logout").status_code == 200
    # Even if someone kept a copy of the cookie, it no longer works.
    client.cookies.set("esw_session", token)
    assert client.get(ME).status_code == 401


def test_expired_session_is_rejected(client, db, make_user):
    make_user("alex")
    client.post(LOGIN, json={"login": "alex", "password": PASSWORD})
    session = db.scalars(select(AuthSession)).one()
    session.expires_at = datetime.now(UTC) - timedelta(seconds=1)
    db.commit()
    assert client.get(ME).status_code == 401


def test_non_active_accounts_cannot_log_in(client, make_user):
    for i, status in enumerate(
        [AccountStatus.SUSPENDED, AccountStatus.INACTIVE, AccountStatus.INVITED]
    ):
        make_user(f"user{i}", status=status)
        r = client.post(LOGIN, json={"login": f"user{i}", "password": PASSWORD})
        assert r.status_code == 403
        assert r.json()["error"]["code"] == "account_inactive"


def test_repeated_failed_logins_are_throttled(client, make_user):
    make_user("alex")
    for _ in range(8):
        client.post(LOGIN, json={"login": "alex", "password": "wrong-pass-1"})
    r = client.post(LOGIN, json={"login": "alex", "password": PASSWORD})
    assert r.status_code == 429


def test_validation_errors_do_not_echo_passwords(client):
    r = client.post(LOGIN, json={"login": "", "password": "my-secret-value"})
    assert r.status_code == 422
    assert "my-secret-value" not in r.text
    assert r.json()["error"]["code"] == "validation_error"


def test_cross_origin_state_change_is_blocked(client, make_user):
    make_user("alex")
    r = client.post(
        LOGIN,
        json={"login": "alex", "password": PASSWORD},
        headers={"Origin": "https://evil.example"},
    )
    assert r.status_code == 403
    ok = client.post(
        LOGIN,
        json={"login": "alex", "password": PASSWORD},
        headers={"Origin": "http://localhost:3000"},
    )
    assert ok.status_code == 200


def test_change_password_revokes_sessions(login_as, new_client):
    c, _ = login_as("alex")
    r = c.post(
        "/api/v1/auth/change-password",
        json={"current_password": PASSWORD, "new_password": "Brand-new-456"},
    )
    assert r.status_code == 200
    assert c.get(ME).status_code == 401
    other = new_client()
    assert other.post(LOGIN, json={"login": "alex", "password": PASSWORD}).status_code == 401
    assert other.post(LOGIN, json={"login": "alex", "password": "Brand-new-456"}).status_code == 200


def test_password_reset_request_does_not_reveal_accounts(client, db, make_user):
    make_user("alex")
    known = client.post("/api/v1/auth/password-reset/request", json={"login": "alex"})
    unknown = client.post("/api/v1/auth/password-reset/request", json={"login": "nobody"})
    assert known.status_code == unknown.status_code == 202
    assert known.json() == unknown.json()
    assert "token" not in known.text
    assert db.scalars(select(PasswordResetToken)).one()


def test_reset_token_is_single_use_and_expires(login_as, new_client, db):
    admin_client, _ = login_as("boss", role=UserRole.ADMIN)
    student_client, student = login_as("alex")
    token = admin_client.post(f"/api/v1/admin/students/{student.id}/password-reset").json()["token"]

    confirm = "/api/v1/auth/password-reset/confirm"
    weak = new_client().post(confirm, json={"token": token, "new_password": "short"})
    assert weak.status_code == 422
    assert (
        new_client()
        .post(confirm, json={"token": token, "new_password": "Reset-pass-789"})
        .status_code
        == 200
    )
    # Old sessions are revoked, token cannot be reused.
    assert student_client.get(ME).status_code == 401
    again = new_client().post(confirm, json={"token": token, "new_password": "Another-pass-1"})
    assert again.status_code == 400

    token2 = admin_client.post(f"/api/v1/admin/students/{student.id}/password-reset").json()[
        "token"
    ]
    record = db.scalar(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == hash_token(token2))
    )
    record.expires_at = datetime.now(UTC) - timedelta(minutes=1)
    db.commit()
    expired = new_client().post(confirm, json={"token": token2, "new_password": "Another-pass-1"})
    assert expired.status_code == 400


def test_user_record_has_role_student_by_default(db, make_user):
    user = make_user("alex")
    assert db.get(User, user.id).role == UserRole.STUDENT
