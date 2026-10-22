from sqlalchemy import inspect

from app.models import Base

EXPECTED_TABLES = {
    "users",
    "auth_sessions",
    "password_reset_tokens",
    "courses",
    "course_levels",
    "units",
    "lessons",
    "learning_items",
    "lesson_learning_items",
    "exercises",
    "exercise_learning_items",
    "media_assets",
    "story_episodes",
    "enrollments",
    "lesson_progress",
    "exercise_attempts",
    "learner_mastery",
    "review_queue",
    "audit_logs",
}


def test_health_endpoint_reports_database(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_openapi_is_served_under_api_prefix(client):
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "English Story World API"


def test_migrations_create_every_model_table():
    from app.db.session import engine

    tables = set(inspect(engine).get_table_names())
    assert EXPECTED_TABLES <= tables
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_exercise_answers_stored_separately_from_public_prompt():
    from app.db.session import engine

    columns = {c["name"] for c in inspect(engine).get_columns("exercises")}
    assert {"prompt", "answer", "feedback", "version"} <= columns
