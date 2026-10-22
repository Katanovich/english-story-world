from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.models import Enrollment, ExerciseAttempt, ReviewQueue
from app.models.enums import UserRole
from tests.conftest import PASSWORD
from tests.factories import build_world, enroll


def _setup(db, login_as, name="alex"):
    world = build_world(db)
    client, user = login_as(name)
    enroll(db, user, world.course)
    return world, client, user


def _submit(client, exercise, response):
    return client.post(f"/api/v1/exercises/{exercise.id}/attempts", json={"response": response})


def test_lesson_loads_without_answer_keys(db, login_as):
    w, c, _ = _setup(db, login_as)
    r = c.get(f"/api/v1/lessons/{w.lessons[0].id}")
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "Lesson 1" and body["next_lesson_id"] == str(w.lessons[1].id)
    assert {e["key"] for e in body["exercises"]} == {"choice", "build", "quiz", "speak"}
    for e in body["exercises"]:
        assert "answer" not in e and "feedback" not in e
    answer_keys = {"accepted", "correct", "blanks", "pairs", "order"}
    for e in body["exercises"]:
        assert not answer_keys & set(e["prompt"])
    assert body["content"]["reading"]["title"] == "Hi"
    assert {i["role"] for i in body["items"]} == {"NEW"}


def test_lesson_without_video_works(db, login_as):
    w, c, _ = _setup(db, login_as)
    episodes = c.get(f"/api/v1/lessons/{w.lessons[0].id}").json()["episodes"]
    assert episodes[0]["has_video"] is False and episodes[0]["video_asset_id"] is None


def test_lesson_access_rules(db, login_as, make_user):
    w = build_world(db)
    outsider, _ = login_as("outsider")  # not enrolled
    assert outsider.get(f"/api/v1/lessons/{w.lessons[0].id}").status_code == 404
    student, user = login_as("alex")
    enroll(db, user, w.course)
    assert student.get(f"/api/v1/lessons/{w.draft.id}").status_code == 404
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    preview = admin.get(f"/api/v1/lessons/{w.draft.id}")
    assert preview.status_code == 200 and preview.json()["is_published"] is False
    # Admin preview never records attempts.
    assert _submit(admin, w.ex["choice"], {"choice": "a"}).status_code == 403


def test_answers_are_validated_on_server_and_persisted(db, login_as):
    w, c, user = _setup(db, login_as)
    wrong = _submit(c, w.ex["choice"], {"choice": "b"})
    assert wrong.status_code == 201
    assert wrong.json()["is_correct"] is False and wrong.json()["solution"] is None
    assert wrong.json()["explanation"] == "Look closely."  # hint only
    # Client cannot claim correctness.
    bad = c.post(
        f"/api/v1/exercises/{w.ex['choice'].id}/attempts",
        json={"response": {"choice": "b"}, "is_correct": True},
    )
    assert bad.status_code == 422
    malformed = _submit(c, w.ex["choice"], {"value": True})
    assert malformed.status_code == 422

    second_wrong = _submit(c, w.ex["choice"], {"choice": "b"}).json()
    assert second_wrong["solution"] == {"correct": "a"}  # revealed after 2 wrong tries

    attempts = db.scalars(select(ExerciseAttempt).where(ExerciseAttempt.user_id == user.id)).all()
    assert len(attempts) == 2
    assert attempts[0].exercise_version == 1
    assert attempts[0].exercise_snapshot["answer"] == {"correct": "a"}
    assert attempts[0].response == {"choice": "b"}


def test_completing_all_exercises_completes_lesson_and_advances(db, login_as):
    w, c, user = _setup(db, login_as)
    assert c.post(f"/api/v1/lessons/{w.lessons[0].id}/start").json()["status"] == "IN_PROGRESS"
    _submit(c, w.ex["choice"], {"choice": "a"})
    _submit(c, w.ex["build"], {"tiles": ["This", "is", "my", "mother"]})
    r = _submit(c, w.ex["quiz"], {"answers": ["father"]})
    assert r.json()["lesson_progress"]["status"] == "IN_PROGRESS"  # speaking not tried yet
    r = _submit(c, w.ex["speak"], {"self_check": True})
    assert r.json()["is_correct"] is None
    progress = r.json()["lesson_progress"]
    assert progress["status"] == "COMPLETED"
    assert progress["score"] == progress["max_score"] == 4
    assert progress["best_quiz_percent"] == 100.0

    enrollment = db.scalar(select(Enrollment).where(Enrollment.user_id == user.id))
    db.refresh(enrollment)
    assert enrollment.current_lesson_id == w.lessons[1].id

    dash = c.get("/api/v1/me/dashboard").json()
    assert dash["lessons_completed"] == 1 and dash["lessons_total"] == 2
    assert dash["current_lesson"]["id"] == str(w.lessons[1].id)
    assert dash["items_practiced"] == 2 and dash["items_mastered"] == 0
    assert {a["key"]: a["earned"] for a in dash["achievements"]}["first_lesson"] is True


def test_progress_survives_logout_and_login(db, login_as, new_client):
    w, c, _ = _setup(db, login_as)
    _submit(c, w.ex["choice"], {"choice": "a"})
    c.post("/api/v1/auth/logout")
    assert c.get("/api/v1/me/progress").status_code == 401
    c2 = new_client()
    c2.post("/api/v1/auth/login", json={"login": "alex", "password": PASSWORD})
    lesson = c2.get(f"/api/v1/lessons/{w.lessons[0].id}").json()
    assert lesson["progress"]["attempted_exercise_ids"] == [str(w.ex["choice"].id)]
    report = c2.get("/api/v1/me/progress").json()
    assert report["lessons"][0]["score"] == 1


def test_students_only_see_their_own_data(db, login_as):
    w, alex, alex_user = _setup(db, login_as, "alex")
    mia, mia_user = login_as("mia")
    enroll(db, mia_user, w.course)
    _submit(alex, w.ex["choice"], {"choice": "a"})

    assert mia.get("/api/v1/me/progress").json() == {"lessons": [], "mastery": []}
    assert mia.get("/api/v1/me/attempts").json()["total"] == 0
    assert mia.get(f"/api/v1/admin/students/{alex_user.id}/progress").status_code == 403
    lesson = mia.get(f"/api/v1/lessons/{w.lessons[0].id}").json()
    assert lesson["progress"] is None
    # Admin can inspect Alex.
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    report = admin.get(f"/api/v1/admin/students/{alex_user.id}/progress").json()
    assert len(report["recent_attempts"]) == 1 and report["lessons"][0]["score"] == 1


def test_review_scheduling_through_the_api(db, login_as):
    w, c, user = _setup(db, login_as)
    before = datetime.now(UTC)
    _submit(c, w.ex["quiz"], {"answers": ["table"]})  # wrong -> father due soon
    _submit(c, w.ex["choice"], {"choice": "a"})  # right -> mother due in ~1 day
    q = {
        r.learning_item_id: r
        for r in db.scalars(select(ReviewQueue).where(ReviewQueue.user_id == user.id))
    }
    father, mother = q[w.items["father"].id], q[w.items["mother"].id]
    assert father.due_at < before + timedelta(minutes=15)
    assert mother.due_at > before + timedelta(hours=23)

    # Immediate retry after feedback is stored but not counted as new evidence.
    retry = _submit(c, w.ex["quiz"], {"answers": ["father"]}).json()
    assert retry["is_correct"] is True and retry["counted_for_mastery"] is False

    father.due_at = datetime.now(UTC) - timedelta(minutes=1)
    db.commit()
    due = c.get("/api/v1/me/review").json()
    assert [d["item"]["key"] for d in due] == ["vocab.father"]
    assert due[0]["exercise"]["key"] == "quiz" and "answer" not in due[0]["exercise"]

    mastery = c.get("/api/v1/me/progress").json()["mastery"]
    assert all(m["mastered"] is False for m in mastery)


def test_suspended_student_loses_lesson_access(db, login_as):
    w, c, user = _setup(db, login_as)
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    admin.post(f"/api/v1/admin/students/{user.id}/status", json={"status": "SUSPENDED"})
    assert c.get(f"/api/v1/lessons/{w.lessons[0].id}").status_code in (401, 403)
    assert _submit(c, w.ex["choice"], {"choice": "a"}).status_code in (401, 403)


def test_admin_enrolls_student(db, login_as):
    w = build_world(db)
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    student, user = login_as("alex")
    assert student.get(f"/api/v1/lessons/{w.lessons[0].id}").status_code == 404
    r = admin.put(
        f"/api/v1/admin/students/{user.id}/enrollment",
        json={"course_id": str(w.course.id), "cefr_level": "A1"},
    )
    assert r.status_code == 200
    assert student.get(f"/api/v1/lessons/{w.lessons[0].id}").status_code == 200
    courses = student.get("/api/v1/me/courses").json()
    assert courses[0]["current_level"] == "A1"
    lesson_titles = [lsn["title"] for lsn in courses[0]["levels"][0]["units"][0]["lessons"]]
    assert lesson_titles == ["Lesson 1", "Lesson 2"]  # draft hidden


def test_my_episodes_lists_published_episodes_of_enrolled_courses(db, login_as):
    w, c, _ = _setup(db, login_as)
    eps = c.get("/api/v1/me/episodes").json()
    assert [(e["title"], e["has_video"]) for e in eps] == [("Meet the family", False)]
    outsider, _ = login_as("outsider")
    assert outsider.get("/api/v1/me/episodes").json() == []
