from sqlalchemy import select

from app.models import AuditLog, Exercise, ExerciseAttempt
from app.models.enums import UserRole
from tests.factories import build_world, enroll

MC = {
    "key": "new-mc",
    "type": "MULTIPLE_CHOICE",
    "section": "QUIZ",
    "instructions": "Choose.",
    "prompt": {
        "question": "Who?",
        "options": [{"id": "a", "text": "mother"}, {"id": "b", "text": "dog"}],
    },
    "answer": {"correct": "a"},
    "feedback": {"hint": "A person."},
}


def _admin(login_as):
    return login_as("boss", role=UserRole.ADMIN)[0]


def test_cms_routes_are_admin_only(db, login_as):
    w = build_world(db)
    student, user = login_as("alex")
    enroll(db, user, w.course)
    for method, path in [
        ("get", "/api/v1/admin/courses"),
        ("get", f"/api/v1/admin/lessons/{w.lessons[0].id}"),
        ("post", f"/api/v1/admin/lessons/{w.lessons[0].id}/publish"),
        ("patch", f"/api/v1/admin/exercises/{w.ex['choice'].id}"),
        ("get", "/api/v1/admin/learning-items"),
        ("get", "/api/v1/admin/audit-logs"),
        ("get", "/api/v1/admin/overview"),
    ]:
        r = getattr(student, method)(path, **({"json": {}} if method != "get" else {}))
        assert r.status_code == 403, path


def test_admin_lesson_view_includes_answers_but_student_view_does_not(db, login_as):
    w = build_world(db)
    admin = _admin(login_as)
    body = admin.get(f"/api/v1/admin/lessons/{w.lessons[0].id}").json()
    choice = next(e for e in body["exercises"] if e["key"] == "choice")
    assert choice["answer"] == {"correct": "a"} and choice["learning_item_ids"]


def test_build_course_structure_and_publish_flow(db, login_as):
    admin = _admin(login_as)
    course_id = admin.post("/api/v1/admin/courses", json={"slug": "new", "title": "New"}).json()[
        "id"
    ]
    assert (
        admin.post("/api/v1/admin/courses", json={"slug": "new", "title": "Dup"}).status_code == 409
    )
    level_id = admin.post(
        f"/api/v1/admin/courses/{course_id}/levels", json={"cefr_level": "A2", "title": "A2"}
    ).json()["id"]
    unit_id = admin.post(
        f"/api/v1/admin/levels/{level_id}/units", json={"slug": "u", "title": "U"}
    ).json()["id"]
    lesson = admin.post(
        f"/api/v1/admin/units/{unit_id}/lessons", json={"slug": "l", "title": "L"}
    ).json()
    assert lesson["status"] == "DRAFT" and lesson["cefr_level"] == "A2"
    lid = lesson["id"]

    report = admin.get(f"/api/v1/admin/lessons/{lid}/validation").json()
    assert any("цель" in e for e in report["errors"]) and any(
        "упражнения" in e for e in report["errors"]
    )
    r = admin.post(f"/api/v1/admin/lessons/{lid}/publish")
    assert r.status_code == 422 and r.json()["error"]["details"]

    bad = admin.patch(f"/api/v1/admin/lessons/{lid}", json={"content": {"reading": {"title": "x"}}})
    assert bad.status_code == 422
    ok = admin.patch(
        f"/api/v1/admin/lessons/{lid}",
        json={
            "objectives": ["Say hi", " "],
            "content": {"reading": {"title": "Hi", "paragraphs": [{"sentences": ["Hi!"]}]}},
        },
    )
    assert ok.status_code == 200 and ok.json()["objectives"] == ["Say hi"]
    bad_ex = dict(MC, answer={"correct": "z"})
    r = admin.post(f"/api/v1/admin/lessons/{lid}/exercises", json=bad_ex)
    assert r.status_code == 422 and "option ids" in str(r.json()["error"]["details"])
    assert admin.post(f"/api/v1/admin/lessons/{lid}/exercises", json=MC).status_code == 201

    r = admin.post(f"/api/v1/admin/lessons/{lid}/publish")
    assert r.status_code == 200 and r.json()["status"] == "PUBLISHED"
    tree = admin.get("/api/v1/admin/courses").json()
    node = tree[0]["levels"][0]["units"][0]["lessons"][0]
    assert node["status"] == "PUBLISHED" and node["exercise_count"] == 1

    actions = set(db.scalars(select(AuditLog.action)))
    assert {"course.create", "lesson.create", "exercise.create", "lesson.publish"} <= actions


def test_editing_answer_bumps_versions_and_keeps_history(db, login_as):
    w = build_world(db)
    admin = _admin(login_as)
    student, user = login_as("alex")
    enroll(db, user, w.course)
    ex = w.ex["choice"]
    student.post(f"/api/v1/exercises/{ex.id}/attempts", json={"response": {"choice": "a"}})

    r = admin.patch(f"/api/v1/admin/exercises/{ex.id}", json={"answer": {"correct": "b"}})
    assert r.status_code == 200 and r.json()["version"] == 2 and r.json()["attempt_count"] == 1
    lesson = admin.get(f"/api/v1/admin/lessons/{w.lessons[0].id}").json()
    assert lesson["content_version"] == 2  # live lesson changed
    # Non-scoring edit does not create a new version.
    r = admin.patch(f"/api/v1/admin/exercises/{ex.id}", json={"instructions": "Pick one."})
    assert r.json()["version"] == 2

    attempt = db.scalar(select(ExerciseAttempt))
    assert attempt.exercise_version == 1 and attempt.exercise_snapshot["answer"] == {"correct": "a"}
    # Exercises with attempts cannot be deleted; unanswered ones can.
    assert admin.delete(f"/api/v1/admin/exercises/{ex.id}").status_code == 409
    quiz_id = w.ex["quiz"].id
    assert admin.delete(f"/api/v1/admin/exercises/{quiz_id}").status_code == 204
    db.expire_all()
    assert db.get(Exercise, quiz_id) is None


def test_unpublish_hides_lesson_but_keeps_progress(db, login_as):
    w = build_world(db)
    admin = _admin(login_as)
    student, user = login_as("alex")
    enroll(db, user, w.course)
    student.post(
        f"/api/v1/exercises/{w.ex['choice'].id}/attempts", json={"response": {"choice": "a"}}
    )
    assert (
        admin.post(f"/api/v1/admin/lessons/{w.lessons[0].id}/unpublish").json()["status"] == "DRAFT"
    )
    assert student.get(f"/api/v1/lessons/{w.lessons[0].id}").status_code == 404
    assert student.get("/api/v1/me/progress").json()["lessons"][0]["score"] == 1
    assert admin.post(f"/api/v1/admin/lessons/{w.lessons[0].id}/publish").status_code == 200
    assert student.get(f"/api/v1/lessons/{w.lessons[0].id}").status_code == 200


def test_learning_items_and_lesson_links(db, login_as):
    w = build_world(db)
    admin = _admin(login_as)
    r = admin.post(
        "/api/v1/admin/learning-items",
        json={"key": "vocab.cat", "kind": "VOCABULARY", "text": "cat", "emoji": "🐱"},
    )
    assert r.status_code == 201
    item_id = r.json()["id"]
    assert (
        admin.post(
            "/api/v1/admin/learning-items",
            json={"key": "vocab.cat", "kind": "VOCABULARY", "text": "x"},
        ).status_code
        == 409
    )
    assert admin.get("/api/v1/admin/learning-items", params={"q": "cat"}).json()["total"] == 1
    r = admin.put(
        f"/api/v1/admin/lessons/{w.lessons[1].id}/items",
        json=[{"learning_item_id": item_id, "role": "NEW"}],
    )
    assert r.status_code == 200 and r.json()["items"] == [
        {"learning_item_id": item_id, "role": "NEW"}
    ]
    r = admin.patch(
        f"/api/v1/admin/exercises/{w.ex['l2'].id}", json={"learning_item_ids": [item_id]}
    )
    assert r.json()["learning_item_ids"] == [item_id]


def test_episode_crud_and_overview(db, login_as):
    w = build_world(db)
    admin = _admin(login_as)
    r = admin.post(f"/api/v1/admin/lessons/{w.lessons[1].id}/episodes", json={"title": "Ep 2"})
    assert r.status_code == 201 and r.json()["status"] == "DRAFT"
    ep = admin.patch(f"/api/v1/admin/episodes/{r.json()['id']}", json={"status": "PUBLISHED"})
    assert ep.json()["status"] == "PUBLISHED"
    ov = admin.get("/api/v1/admin/overview").json()
    assert ov["lessons_published"] == 2 and ov["lessons_draft"] == 1
    logs = admin.get("/api/v1/admin/audit-logs", params={"action": "episode"}).json()
    assert logs["total"] == 2 and logs["items"][0]["actor_username"] == "boss"
