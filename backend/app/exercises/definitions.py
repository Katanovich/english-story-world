"""Exercise definitions: per-type prompt/answer/response schemas.

`prompt` is what a learner sees, `answer` is the private answer key. The CMS and the
seed script validate both with `validate_definition` before saving, so the scoring
engine can trust their shape.
"""

import random
import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from app.models.enums import ExerciseType


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Option(_Strict):
    id: str = Field(min_length=1, max_length=40)
    text: str | None = Field(default=None, max_length=300)
    image_id: uuid.UUID | None = None
    # Emoji used as a simple illustration until real artwork is uploaded.
    emoji: str | None = Field(default=None, max_length=16)

    @model_validator(mode="after")
    def _has_content(self) -> "Option":
        if not self.text and not self.image_id and not self.emoji:
            raise ValueError("an option needs text, an image or an emoji")
        return self


# ---- Prompts (public) ---------------------------------------------------------------


class ChoicePrompt(_Strict):
    """MULTIPLE_CHOICE, IMAGE_SELECTION, READING/LISTENING_COMPREHENSION."""

    question: str = Field(min_length=1, max_length=500)
    options: list[Option] = Field(min_length=2, max_length=8)
    # Optional text shown above the question (e.g. a short passage or audio transcript).
    context: str | None = Field(default=None, max_length=2000)
    # Listening comprehension: id of the listening track in lesson.content.listening
    listening_id: str | None = None
    # Short text to play: the audio file if audio_id is set, else browser speech synthesis.
    listen_text: str | None = Field(default=None, max_length=500)
    emoji: str | None = Field(default=None, max_length=16)


class TrueFalsePrompt(_Strict):
    statement: str = Field(min_length=1, max_length=500)
    context: str | None = Field(default=None, max_length=2000)
    listening_id: str | None = None
    listen_text: str | None = Field(default=None, max_length=500)
    emoji: str | None = Field(default=None, max_length=16)


class MatchingPrompt(_Strict):
    left: list[Option] = Field(min_length=2, max_length=8)
    right: list[Option] = Field(min_length=2, max_length=8)


class SentenceBuilderPrompt(_Strict):
    tiles: list[str] = Field(min_length=2, max_length=15)
    hint: str | None = Field(default=None, max_length=300)


class FillBlankPrompt(_Strict):
    # Use "___" for each blank, e.g. "My ___ is Alex."
    text: str = Field(min_length=1, max_length=500)
    word_bank: list[str] = Field(default_factory=list, max_length=12)
    hint_ru: str | None = Field(default=None, max_length=200)

    @property
    def blank_count(self) -> int:
        return self.text.count("___")


class OrderEventsPrompt(_Strict):
    items: list[Option] = Field(min_length=2, max_length=8)


class SpeakingPrompt(_Strict):
    text: str = Field(min_length=1, max_length=500)
    model_answer: str | None = Field(default=None, max_length=500)
    model_audio_id: uuid.UUID | None = None


# ---- Answers (private) --------------------------------------------------------------


class ChoiceAnswer(_Strict):
    correct: str


class TrueFalseAnswer(_Strict):
    correct: bool


class MatchingAnswer(_Strict):
    pairs: dict[str, str]


class AcceptedSentences(_Strict):
    accepted: list[str] = Field(min_length=1)


class FillBlankAnswer(_Strict):
    # One list of accepted answers per blank.
    blanks: list[list[str]] = Field(min_length=1)


class OrderAnswer(_Strict):
    order: list[str] = Field(min_length=2)


class EmptyAnswer(_Strict):
    pass


# ---- Responses (what the learner submits) -------------------------------------------


class ChoiceResponse(_Strict):
    choice: str = Field(max_length=40)


class TrueFalseResponse(_Strict):
    value: bool


class MatchingResponse(_Strict):
    pairs: dict[str, str] = Field(max_length=8)


class SentenceResponse(_Strict):
    tiles: list[str] = Field(max_length=15)


class FillBlankResponse(_Strict):
    answers: list[str] = Field(max_length=10)


class OrderResponse(_Strict):
    order: list[str] = Field(max_length=8)


class SpeakingResponse(_Strict):
    recording_asset_id: uuid.UUID | None = None
    # Learner's own "I said it" check. Not an automatic evaluation.
    self_check: bool | None = None


CHOICE_TYPES = {
    ExerciseType.MULTIPLE_CHOICE,
    ExerciseType.IMAGE_SELECTION,
    ExerciseType.READING_COMPREHENSION,
    ExerciseType.LISTENING_COMPREHENSION,
}

SCHEMAS: dict[ExerciseType, tuple[type[_Strict], type[_Strict], type[_Strict]]] = {
    **{t: (ChoicePrompt, ChoiceAnswer, ChoiceResponse) for t in CHOICE_TYPES},
    ExerciseType.TRUE_FALSE: (TrueFalsePrompt, TrueFalseAnswer, TrueFalseResponse),
    ExerciseType.MATCHING: (MatchingPrompt, MatchingAnswer, MatchingResponse),
    ExerciseType.SENTENCE_BUILDER: (SentenceBuilderPrompt, AcceptedSentences, SentenceResponse),
    ExerciseType.FILL_BLANK: (FillBlankPrompt, FillBlankAnswer, FillBlankResponse),
    ExerciseType.ORDER_EVENTS: (OrderEventsPrompt, OrderAnswer, OrderResponse),
    ExerciseType.SPEAKING: (SpeakingPrompt, EmptyAnswer, SpeakingResponse),
}


class DefinitionError(ValueError):
    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


def _cross_check(ex_type: ExerciseType, prompt: Any, answer: Any) -> list[str]:
    errors: list[str] = []
    if ex_type in CHOICE_TYPES:
        ids = [o.id for o in prompt.options]
        if len(set(ids)) != len(ids):
            errors.append("option ids must be unique")
        if answer.correct not in ids:
            errors.append("correct answer must be one of the option ids")
    elif ex_type == ExerciseType.MATCHING:
        left = {o.id for o in prompt.left}
        right = {o.id for o in prompt.right}
        if set(answer.pairs) != left:
            errors.append("every left item needs exactly one pair")
        if not set(answer.pairs.values()) <= right:
            errors.append("pairs must point to right item ids")
    elif ex_type == ExerciseType.SENTENCE_BUILDER:
        tiles = sorted(normalize(t) for t in prompt.tiles)
        for sentence in answer.accepted:
            if sorted(tokenize(sentence)) != tiles:
                errors.append(f"accepted sentence '{sentence}' must use exactly the given tiles")
    elif ex_type == ExerciseType.FILL_BLANK:
        if prompt.blank_count == 0:
            errors.append("text must contain at least one ___ blank")
        if prompt.blank_count != len(answer.blanks):
            errors.append("number of blanks and answers must match")
    elif ex_type == ExerciseType.ORDER_EVENTS:
        ids = [o.id for o in prompt.items]
        if sorted(ids) != sorted(answer.order) or len(set(ids)) != len(ids):
            errors.append("order must contain every item id exactly once")
    return errors


def validate_definition(
    ex_type: ExerciseType, prompt: dict[str, Any], answer: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate and normalise a prompt/answer pair. Raises DefinitionError."""
    prompt_cls, answer_cls, _ = SCHEMAS[ex_type]
    try:
        p = prompt_cls.model_validate(prompt)
        a = answer_cls.model_validate(answer)
    except ValidationError as exc:
        raise DefinitionError(
            [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()]
        ) from exc
    errors = _cross_check(ex_type, p, a)
    if errors:
        raise DefinitionError(errors)
    return p.model_dump(mode="json", exclude_none=True), a.model_dump(mode="json")


def parse_response(ex_type: ExerciseType, response: dict[str, Any]) -> Any:
    return SCHEMAS[ex_type][2].model_validate(response)


def public_prompt(ex_type: ExerciseType, prompt: dict[str, Any]) -> dict[str, Any]:
    """Prompt as served to learners: orderable items are shuffled so the stored order
    (which may match the answer) is never revealed."""
    data = dict(prompt)
    rng = random.SystemRandom()
    if ex_type == ExerciseType.SENTENCE_BUILDER:
        data["tiles"] = rng.sample(prompt["tiles"], len(prompt["tiles"]))
    elif ex_type == ExerciseType.ORDER_EVENTS:
        data["items"] = rng.sample(prompt["items"], len(prompt["items"]))
    elif ex_type == ExerciseType.MATCHING:
        data["right"] = rng.sample(prompt["right"], len(prompt["right"]))
    return data


# ---- Text normalisation -------------------------------------------------------------

_PUNCT = str.maketrans({c: " " for c in '.,!?;:"()'})


def normalize(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").lower().translate(_PUNCT)
    return " ".join(text.split())


def tokenize(sentence: str) -> list[str]:
    return normalize(sentence).split()
