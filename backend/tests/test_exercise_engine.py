from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.exercises.definitions import DefinitionError, public_prompt, validate_definition
from app.exercises.scoring import score_response
from app.models import LearnerMastery, ReviewQueue
from app.models.enums import ExerciseType as T
from app.services.learning import (
    MASTERED_THRESHOLD,
    RELEARN_DELAY,
    START_EASE,
    estimate_mastery,
    next_schedule,
)

OPTS = [{"id": "a", "text": "dog"}, {"id": "b", "text": "cat"}]


@pytest.mark.parametrize(
    ("ex_type", "answer", "response", "expected"),
    [
        (T.MULTIPLE_CHOICE, {"correct": "a"}, {"choice": "a"}, True),
        (T.IMAGE_SELECTION, {"correct": "a"}, {"choice": "b"}, False),
        (T.TRUE_FALSE, {"correct": False}, {"value": False}, True),
        (
            T.SENTENCE_BUILDER,
            {"accepted": ["I have a dog."]},
            {"tiles": ["I", "have", "a", "dog"]},
            True,
        ),
        (
            T.SENTENCE_BUILDER,
            {"accepted": ["I have a dog."]},
            {"tiles": ["a", "dog", "I", "have"]},
            False,
        ),
        (T.FILL_BLANK, {"blanks": [["under"]]}, {"answers": ["  Under "]}, True),
        (T.FILL_BLANK, {"blanks": [["under"]]}, {"answers": ["on"]}, False),
        (T.ORDER_EVENTS, {"order": ["1", "2", "3"]}, {"order": ["1", "2", "3"]}, True),
        (T.ORDER_EVENTS, {"order": ["1", "2", "3"]}, {"order": ["2", "1", "3"]}, False),
    ],
)
def test_objective_types_are_scored_on_the_server(ex_type, answer, response, expected):
    result = score_response(ex_type, answer, response, points=2)
    assert result.is_correct is expected
    assert result.score == (2 if expected else 0)
    assert result.max_score == 2


def test_matching_gives_partial_credit_but_is_only_correct_when_complete():
    key = {"pairs": {"dog": "1", "cat": "2"}}
    full = score_response(T.MATCHING, key, {"pairs": {"dog": "1", "cat": "2"}}, points=2)
    half = score_response(T.MATCHING, key, {"pairs": {"dog": "1", "cat": "1"}}, points=2)
    assert full.is_correct and full.score == 2
    assert half.is_correct is False and half.score == 1
    assert half.details == {"pairs": {"dog": True, "cat": False}}


def test_speaking_is_never_automatically_evaluated():
    result = score_response(T.SPEAKING, {}, {"self_check": True}, points=3)
    assert result.is_correct is None and result.score == 0 and result.max_score == 0


def test_malformed_responses_are_rejected():
    with pytest.raises(ValidationError):
        score_response(T.MULTIPLE_CHOICE, {"correct": "a"}, {"choice": "a", "is_correct": True}, 1)
    with pytest.raises(ValidationError):
        score_response(T.TRUE_FALSE, {"correct": True}, {"value": "maybe"}, 1)


def test_definitions_are_cross_checked():
    with pytest.raises(DefinitionError, match="one of the option ids"):
        validate_definition(T.MULTIPLE_CHOICE, {"question": "?", "options": OPTS}, {"correct": "z"})
    with pytest.raises(DefinitionError, match="exactly the given tiles"):
        validate_definition(T.SENTENCE_BUILDER, {"tiles": ["I", "am"]}, {"accepted": ["I am Mia"]})
    with pytest.raises(DefinitionError, match="blanks and answers"):
        validate_definition(T.FILL_BLANK, {"text": "I ___ a ___."}, {"blanks": [["am"]]})
    with pytest.raises(DefinitionError):
        validate_definition(
            T.MULTIPLE_CHOICE, {"question": "?", "options": OPTS, "answer": "a"}, {"correct": "a"}
        )


def test_public_prompt_contains_no_answer_and_keeps_tiles():
    prompt, _ = validate_definition(
        T.SENTENCE_BUILDER, {"tiles": ["I", "am", "Mia"]}, {"accepted": ["I am Mia."]}
    )
    shown = public_prompt(T.SENTENCE_BUILDER, prompt)
    assert sorted(shown["tiles"]) == sorted(prompt["tiles"])
    assert "accepted" not in shown


def _queue():
    return ReviewQueue(interval_days=0.0, ease=START_EASE, repetitions=0)


def test_schedule_extends_interval_after_success_and_resets_after_error():
    now = datetime.now(UTC)
    q = _queue()
    intervals = []
    for _ in range(4):
        next_schedule(q, True, now)
        intervals.append(q.interval_days)
    assert intervals[0] == 1 and intervals[1] == 3
    assert intervals[3] > intervals[2] > intervals[1]
    ease_before = q.ease
    next_schedule(q, False, now)
    assert q.repetitions == 0 and q.ease < ease_before
    assert q.due_at == now + RELEARN_DELAY


def _m(**kw):
    base = dict(attempts=0, correct=0, incorrect=0, recognition_correct=0, recall_correct=0)
    base.update(kw)
    return LearnerMastery(**base)


def test_one_correct_picture_choice_is_not_mastery():
    assert estimate_mastery(_m(attempts=1, correct=1, recognition_correct=1)) < 0.2
    # Lots of recognition alone never reaches the mastered threshold.
    assert (
        estimate_mastery(_m(attempts=10, correct=10, recognition_correct=10)) < MASTERED_THRESHOLD
    )
    strong = _m(attempts=6, correct=6, recognition_correct=3, recall_correct=3)
    assert estimate_mastery(strong) >= MASTERED_THRESHOLD
    shaky = _m(attempts=12, correct=6, incorrect=6, recognition_correct=3, recall_correct=3)
    assert estimate_mastery(shaky) < MASTERED_THRESHOLD


def test_relearn_delay_is_short():
    assert RELEARN_DELAY <= timedelta(minutes=30)
