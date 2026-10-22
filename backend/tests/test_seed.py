from collections import Counter

from sqlalchemy import func, select

from app.models import (
    Course,
    Enrollment,
    Exercise,
    ExerciseAttempt,
    LearningItem,
    Lesson,
    LessonLearningItem,
    StoryEpisode,
)
from app.models.enums import ExerciseType, LessonItemRole, LessonSection
from app.seed import load_seed_data
from app.seed import run_seed as _run_seed
from app.seed.characters import ROLES

DEFAULT_NAMES = {role: default for role, (default, _) in ROLES.items()}
# Tests always use the public default names, regardless of any local names file.
DATA = load_seed_data(DEFAULT_NAMES)
ALL_LESSONS = [lesson for _, _, lesson in DATA.lessons()]


def run_seed(db, update=False):
    return _run_seed(db, update=update, data=DATA)


TABLES = [Course, Lesson, LearningItem, Exercise, LessonLearningItem, StoryEpisode]


def _counts(db):
    return {m.__tablename__: db.scalar(select(func.count()).select_from(m)) for m in TABLES}


def _lessons(db):
    """Lessons in course order (level, unit, lesson position)."""
    from app.models import CourseLevel, Unit

    return list(
        db.scalars(
            select(Lesson)
            .join(Unit, Unit.id == Lesson.unit_id)
            .join(CourseLevel, CourseLevel.id == Unit.level_id)
            .order_by(CourseLevel.position, Unit.position, Lesson.position)
        )
    )


def correct_response(ex: Exercise) -> dict:
    a = ex.answer
    match ex.type:
        case ExerciseType.TRUE_FALSE:
            return {"value": a["correct"]}
        case ExerciseType.MATCHING:
            return {"pairs": a["pairs"]}
        case ExerciseType.SENTENCE_BUILDER:
            return {"tiles": a["accepted"][0].rstrip(".?!").split()}
        case ExerciseType.FILL_BLANK:
            return {"answers": [b[0] for b in a["blanks"]]}
        case ExerciseType.ORDER_EVENTS:
            return {"order": a["order"]}
        case ExerciseType.SPEAKING:
            return {"self_check": True}
        case _:
            return {"choice": a["correct"]}


def test_seed_is_repeatable_without_duplicates(db):
    first = run_seed(db)
    counts = _counts(db)
    assert counts == {
        "courses": 1,
        "lessons": len(ALL_LESSONS),
        "learning_items": len(DATA.items),
        "exercises": sum(len(lsn["exercises"]) for lsn in ALL_LESSONS),
        "lesson_learning_items": counts["lesson_learning_items"],
        "story_episodes": len(ALL_LESSONS),
    }
    assert first.created["lessons"] == len(ALL_LESSONS) >= 10
    assert run_seed(db).summary() == "created: nothing; updated: nothing"
    run_seed(db, update=True)
    assert _counts(db) == counts


def test_every_lesson_has_required_parts(db):
    run_seed(db)
    for lesson in _lessons(db):
        assert lesson.status == "PUBLISHED" and lesson.objectives and lesson.estimated_minutes > 0
        assert lesson.content["reading"]["paragraphs"]
        assert lesson.content["listening"] and lesson.content["grammar"]
        sections = {e.section for e in lesson.exercises}
        assert sections == set(LessonSection), lesson.slug
        assert len(lesson.episodes) == 1 and lesson.episodes[0].video_asset_id is None
    all_types = {e.type for e in db.scalars(select(Exercise))}
    assert all_types == set(ExerciseType)


def test_cumulative_review_links(db):
    run_seed(db)
    lessons = _lessons(db)
    roles = []
    for lesson in lessons:
        links = db.scalars(
            select(LessonLearningItem).where(LessonLearningItem.lesson_id == lesson.id)
        ).all()
        roles.append(Counter(link.role for link in links))
    assert roles[0][LessonItemRole.NEW] > 0 and roles[0][LessonItemRole.RECENT_REVIEW] == 0
    for r in roles[1:]:
        assert r[LessonItemRole.NEW] > 0 and r[LessonItemRole.RECENT_REVIEW] > 0
    for r in roles[2:]:
        assert r[LessonItemRole.OLDER_REVIEW] > 0
    # Old words are reused, but not every old word in every lesson.
    total_items = len(DATA.items)
    assert all(sum(r.values()) < total_items for r in roles)


def _quiz_sources(db, lesson):
    introduced_in = {
        item.id: item.introduced_in_lesson_id for item in db.scalars(select(LearningItem))
    }
    return {
        introduced_in[link.learning_item_id]
        for e in lesson.exercises
        if e.section == LessonSection.QUIZ
        for link in e.item_links
    }


def test_unit_final_quizzes_are_cumulative(db):
    run_seed(db)
    lessons = _lessons(db)
    # Lesson 5 quiz covers all of unit 1; lesson 10 quiz reaches back into unit 1 too.
    assert _quiz_sources(db, lessons[4]) == {lsn.id for lsn in lessons[:5]}
    sources_10 = _quiz_sources(db, lessons[9])
    assert len(sources_10) >= 5 and sources_10 & {lsn.id for lsn in lessons[:5]}


def test_every_seed_answer_key_scores_correct_through_the_api(db, login_as):
    run_seed(db)
    client, user = login_as("alex")
    course = db.scalar(select(Course))
    db.add(Enrollment(user_id=user.id, course_id=course.id))
    db.commit()
    for lesson in _lessons(db):
        assert client.get(f"/api/v1/lessons/{lesson.id}").status_code == 200
        for ex in lesson.exercises:
            r = client.post(
                f"/api/v1/exercises/{ex.id}/attempts", json={"response": correct_response(ex)}
            )
            assert r.status_code == 201, (lesson.slug, ex.key, r.text)
            assert r.json()["is_correct"] in (True, None), (lesson.slug, ex.key)
        progress = r.json()["lesson_progress"]
        assert progress["status"] == "COMPLETED" and progress["score"] == progress["max_score"]
    dash = client.get("/api/v1/me/dashboard").json()
    n = len(ALL_LESSONS)
    assert dash["lessons_completed"] == n and dash["lessons_total"] == n
    assert dash["items_practiced"] > 30


def test_default_seed_keeps_cms_edits_and_update_bumps_versions(db, login_as):
    run_seed(db)
    lesson = _lessons(db)[0]
    ex = next(e for e in lesson.exercises if e.key == "quiz-hello")

    client, user = login_as("alex")
    db.add(Enrollment(user_id=user.id, course_id=db.scalar(select(Course)).id))
    lesson.title = "Edited in CMS"
    ex.answer = {"correct": "b"}  # simulate a CMS edit
    db.commit()
    client.post(f"/api/v1/exercises/{ex.id}/attempts", json={"response": {"choice": "b"}})

    run_seed(db)  # default mode: no overwrite
    db.refresh(lesson)
    assert lesson.title == "Edited in CMS"

    run_seed(db, update=True)
    db.refresh(lesson)
    db.refresh(ex)
    assert lesson.title == "Meet My Family" and lesson.content_version == 2
    assert ex.answer == {"correct": "a"} and ex.version == 2
    attempt = db.scalar(select(ExerciseAttempt).where(ExerciseAttempt.exercise_id == ex.id))
    # The old attempt still records the version and key it was scored against.
    assert attempt.exercise_version == 1 and attempt.exercise_snapshot["answer"] == {"correct": "b"}
