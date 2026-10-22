import io

from app.models.enums import UserRole
from tests.factories import build_world, enroll

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
MP4 = b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 100
WEBM = b"\x1a\x45\xdf\xa3" + b"\x00" * 100
VTT = b"WEBVTT\n\n00:00.000 --> 00:01.000\nHello!\n"


def _upload(client, name, data, media_type):
    return client.post(
        "/api/v1/admin/media",
        files={"file": (name, io.BytesIO(data), "application/octet-stream")},
        data={"media_type": media_type},
    )


def test_admin_upload_and_authorised_download(login_as):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    r = _upload(admin, "mother.png", PNG, "IMAGE")
    assert r.status_code == 201, r.text
    asset = r.json()
    assert asset["mime_type"] == "image/png" and asset["size_bytes"] == len(PNG)
    assert "mother.png" not in asset["url"]  # storage key is server-generated

    student, _ = login_as("alex")
    got = student.get(asset["url"])
    assert got.status_code == 200 and got.content == PNG
    assert got.headers["x-content-type-options"] == "nosniff"
    student.post("/api/v1/auth/logout")
    assert student.get(asset["url"]).status_code == 401


def test_upload_validates_type_and_content(login_as):
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    assert _upload(admin, "virus.png", b"MZ\x90\x00 not an image", "IMAGE").status_code == 415
    assert _upload(admin, "pic.gif", PNG, "IMAGE").status_code == 415  # extension not allowed
    assert _upload(admin, "x.svg", b"<svg onload=alert(1)>", "IMAGE").status_code == 415
    assert _upload(admin, "clip.mp4", PNG, "VIDEO").status_code == 415  # content mismatch
    assert _upload(admin, "clip.mp4", MP4, "VIDEO").status_code == 201
    assert _upload(admin, "subs.vtt", VTT, "SUBTITLE").status_code == 201


def test_upload_size_limit(login_as, monkeypatch):
    from app.services import media

    monkeypatch.setattr(media, "_limit_bytes", lambda _t: 50)
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    r = _upload(admin, "big.png", PNG, "IMAGE")
    assert r.status_code == 413


def test_students_cannot_upload_content_media(login_as):
    student, _ = login_as("alex")
    assert _upload(student, "mother.png", PNG, "IMAGE").status_code == 403


def test_recordings_are_private(db, login_as):
    w = build_world(db)
    alex, alex_user = login_as("alex")
    mia, mia_user = login_as("mia")
    enroll(db, alex_user, w.course)
    enroll(db, mia_user, w.course)
    rec = alex.post(
        "/api/v1/me/recordings", files={"file": ("voice.webm", io.BytesIO(WEBM), "audio/webm")}
    )
    assert rec.status_code == 201
    rec = rec.json()
    assert alex.get(rec["url"]).status_code == 200
    assert mia.get(rec["url"]).status_code == 404
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    assert admin.get(rec["url"]).status_code == 200
    # Recording is hidden from the content media library.
    assert admin.get("/api/v1/admin/media").json()["total"] == 0

    speak = w.ex["speak"]
    ok = alex.post(
        f"/api/v1/exercises/{speak.id}/attempts",
        json={"response": {"recording_asset_id": rec["id"]}},
    )
    assert ok.status_code == 201 and ok.json()["is_correct"] is None
    stolen = mia.post(
        f"/api/v1/exercises/{speak.id}/attempts",
        json={"response": {"recording_asset_id": rec["id"]}},
    )
    assert stolen.status_code == 404
    # Recordings cannot be attached to lessons as content.
    r = admin.put(
        f"/api/v1/admin/episodes/{w.episode.id}/media", json={"video_asset_id": rec["id"]}
    )
    assert r.status_code == 422


def test_attaching_video_does_not_break_lesson(db, login_as):
    w = build_world(db)
    admin, _ = login_as("boss", role=UserRole.ADMIN)
    student, user = login_as("alex")
    enroll(db, user, w.course)
    video = _upload(admin, "ep1.mp4", MP4, "VIDEO").json()
    subs = _upload(admin, "ep1.vtt", VTT, "SUBTITLE").json()
    image = _upload(admin, "poster.png", PNG, "IMAGE").json()

    wrong = admin.put(
        f"/api/v1/admin/episodes/{w.episode.id}/media", json={"video_asset_id": image["id"]}
    )
    assert wrong.status_code == 422
    r = admin.put(
        f"/api/v1/admin/episodes/{w.episode.id}/media",
        json={"video_asset_id": video["id"], "subtitle_asset_id": subs["id"]},
    )
    assert r.status_code == 200 and r.json()["has_video"] is True

    lesson = student.get(f"/api/v1/lessons/{w.lessons[0].id}")
    assert lesson.status_code == 200
    body = lesson.json()
    assert body["episodes"][0]["has_video"] is True
    assert body["media"][video["id"]]["mime_type"] == "video/mp4"
    assert len(body["exercises"]) == 4  # rest of the lesson unchanged
    ranged = student.get(video["url"], headers={"Range": "bytes=0-9"})
    assert ranged.status_code == 206 and len(ranged.content) == 10
