from sqlalchemy import select

from app.models import AuditLog
from app.models.enums import UserRole
from tests.conftest import PASSWORD

BASE = "/api/v1/admin/students"


def test_student_cannot_access_admin_endpoints(login_as):
    c, student = login_as("alex")
    assert c.get(BASE).status_code == 403
    assert c.post(BASE, json={"username": "mia", "display_name": "Mia"}).status_code == 403
    r = c.post(f"{BASE}/{student.id}/status", json={"status": "ACTIVE"})
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "forbidden"


def test_admin_creates_student_with_password(login_as, new_client):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    r = admin.post(
        BASE, json={"username": "Mia", "display_name": "Mia", "password": "Mia-pass-123"}
    )
    assert r.status_code == 201
    body = r.json()
    assert body["user"]["role"] == "STUDENT" and body["user"]["status"] == "ACTIVE"
    assert body["set_password_token"] is None
    login = new_client().post(
        "/api/v1/auth/login", json={"login": "mia", "password": "Mia-pass-123"}
    )
    assert login.status_code == 200


def test_client_cannot_choose_role_when_creating_user(login_as):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    r = admin.post(BASE, json={"username": "sneaky", "display_name": "S", "role": "ADMIN"})
    assert r.status_code == 422


def test_invited_student_activates_by_setting_password(login_as, new_client):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    body = admin.post(BASE, json={"username": "mia", "display_name": "Mia"}).json()
    assert body["user"]["status"] == "INVITED"
    token = body["set_password_token"]
    c = new_client()
    assert c.post(
        "/api/v1/auth/login", json={"login": "mia", "password": "Whatever-123"}
    ).status_code in (401, 403)
    assert (
        c.post(
            "/api/v1/auth/password-reset/confirm",
            json={"token": token, "new_password": "Mia-pass-123"},
        ).status_code
        == 200
    )
    assert (
        c.post("/api/v1/auth/login", json={"login": "mia", "password": "Mia-pass-123"}).status_code
        == 200
    )


def test_duplicate_username_conflicts(login_as, make_user):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    make_user("mia")
    r = admin.post(
        BASE, json={"username": "MIA", "display_name": "Mia", "password": "Mia-pass-123"}
    )
    assert r.status_code == 409


def test_list_search_filter_and_paginate(login_as, make_user):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    for name in ["alex", "mia", "max"]:
        make_user(name)
    from app.models.enums import AccountStatus

    make_user("sam", status=AccountStatus.SUSPENDED)

    all_ = admin.get(BASE).json()
    assert all_["total"] == 4  # admins are not listed
    assert {u["username"] for u in admin.get(BASE, params={"q": "ma"}).json()["items"]} == {"max"}
    suspended = admin.get(BASE, params={"status": "SUSPENDED"}).json()
    assert [u["username"] for u in suspended["items"]] == ["sam"]
    page = admin.get(BASE, params={"page": 2, "page_size": 3}).json()
    assert page["total"] == 4 and len(page["items"]) == 1


def test_suspension_blocks_access_immediately_and_restore_keeps_account(login_as, new_client, db):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    student_client, student = login_as("alex")
    assert student_client.get("/api/v1/auth/me").status_code == 200

    r = admin.post(f"{BASE}/{student.id}/status", json={"status": "SUSPENDED", "reason": "test"})
    assert r.status_code == 200 and r.json()["status"] == "SUSPENDED"
    assert student_client.get("/api/v1/auth/me").status_code in (401, 403)

    admin.post(f"{BASE}/{student.id}/status", json={"status": "ACTIVE"})
    c = new_client()
    assert (
        c.post("/api/v1/auth/login", json={"login": "alex", "password": PASSWORD}).status_code
        == 200
    )

    actions = db.scalars(select(AuditLog.action).order_by(AuditLog.created_at)).all()
    assert actions.count("student.status_change") == 2


def test_admin_cannot_manage_admin_accounts_via_student_routes(login_as):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    _, other_admin = login_as("boss2", role=UserRole.ADMIN)
    assert admin.get(f"{BASE}/{other_admin.id}").status_code == 404
    r = admin.post(f"{BASE}/{other_admin.id}/status", json={"status": "SUSPENDED"})
    assert r.status_code == 404
