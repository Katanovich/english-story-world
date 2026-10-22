"""Server-side scoring. The client only ever sends a response; correctness is decided here."""

from dataclasses import dataclass, field
from typing import Any

from app.exercises.definitions import CHOICE_TYPES, normalize, parse_response
from app.models.enums import ExerciseType


@dataclass
class ScoreResult:
    is_correct: bool | None  # None = not automatically evaluated (speaking)
    score: int
    max_score: int
    # Per-part correctness (e.g. which blanks/pairs were right) — safe to show after submit.
    details: dict[str, Any] = field(default_factory=dict)


def score_response(
    ex_type: ExerciseType,
    answer: dict[str, Any],
    response: dict[str, Any],
    points: int,
    is_scored: bool = True,
) -> ScoreResult:
    """Score a response against the answer key. Raises pydantic.ValidationError for a
    malformed response."""
    r = parse_response(ex_type, response)

    if ex_type == ExerciseType.SPEAKING or not is_scored:
        return ScoreResult(is_correct=None, score=0, max_score=0)

    if ex_type in CHOICE_TYPES:
        ok = r.choice == answer["correct"]
        return ScoreResult(ok, points if ok else 0, points)

    if ex_type == ExerciseType.TRUE_FALSE:
        ok = r.value == answer["correct"]
        return ScoreResult(ok, points if ok else 0, points)

    if ex_type == ExerciseType.SENTENCE_BUILDER:
        built = normalize(" ".join(r.tiles))
        ok = built in {normalize(s) for s in answer["accepted"]}
        return ScoreResult(ok, points if ok else 0, points)

    if ex_type == ExerciseType.ORDER_EVENTS:
        ok = r.order == answer["order"]
        return ScoreResult(ok, points if ok else 0, points)

    if ex_type == ExerciseType.MATCHING:
        key: dict[str, str] = answer["pairs"]
        per_item = {left: r.pairs.get(left) == right for left, right in key.items()}
        return _partial(per_item, points, "pairs")

    if ex_type == ExerciseType.FILL_BLANK:
        blanks: list[list[str]] = answer["blanks"]
        given = list(r.answers) + [""] * (len(blanks) - len(r.answers))
        per_blank = {
            str(i): normalize(given[i]) in {normalize(a) for a in accepted}
            for i, accepted in enumerate(blanks)
        }
        return _partial(per_blank, points, "blanks")

    raise ValueError(f"Unsupported exercise type {ex_type}")


def _partial(per_part: dict[str, bool], points: int, label: str) -> ScoreResult:
    """Correct only when every part is right; partial credit rounds down."""
    right = sum(per_part.values())
    total = len(per_part)
    ok = right == total
    score = points if ok else (points * right) // total
    return ScoreResult(ok, score, points, {label: per_part})
