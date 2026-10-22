"""Shared builders for seed exercises (see app/exercises/definitions.py for formats)."""

from typing import Any

V, G, P = "VOCABULARY", "GRAMMAR", "PHRASE"

# key -> (kind, text, emoji, translation_ru, introduced_in_lesson_slug, examples, explanation)
Item = tuple[str, str, str | None, str, str, list[str], str | None]

FB_OK = "Great job!"
FB_TRY = "Not yet. Have another try!"


def _fb(hint: str, explanation: str) -> dict[str, str]:
    return {"correct": FB_OK, "incorrect": FB_TRY, "hint": hint, "explanation": explanation}


def _opts(*options: tuple[str | None, str | None]) -> list[dict[str, Any]]:
    """Options from (text, emoji) pairs with ids a, b, c..."""
    out = []
    for i, (text, emoji) in enumerate(options):
        o: dict[str, Any] = {"id": "abcdefgh"[i]}
        if text:
            o["text"] = text
        if emoji:
            o["emoji"] = emoji
        out.append(o)
    return out


def choice(
    key,
    section,
    instructions,
    question,
    options,
    correct,
    items,
    hint,
    expl,
    ex_type="MULTIPLE_CHOICE",
    **extra,
):
    prompt = {"question": question, "options": _opts(*options), **extra}
    return dict(
        key=key,
        type=ex_type,
        section=section,
        mode="RECOGNITION",
        instructions=instructions,
        prompt=prompt,
        answer={"correct": correct},
        items=items,
        feedback=_fb(hint, expl),
        points=1,
    )


def true_false(key, section, instructions, statement, correct, items, hint, expl, **extra):
    return dict(
        key=key,
        type="TRUE_FALSE",
        section=section,
        mode="RECOGNITION",
        instructions=instructions,
        prompt={"statement": statement, **extra},
        answer={"correct": correct},
        items=items,
        feedback=_fb(hint, expl),
        points=1,
    )


def matching(key, section, instructions, pairs, items, hint, expl):
    """pairs: list of (left_text, right_text_or_None, right_emoji_or_None)."""
    left = [{"id": f"l{i}", "text": lt} for i, (lt, _, _) in enumerate(pairs)]
    right = []
    for i, (_, rt, re) in enumerate(pairs):
        o: dict[str, Any] = {"id": f"r{i}"}
        if rt:
            o["text"] = rt
        if re:
            o["emoji"] = re
        right.append(o)
    answer = {"pairs": {f"l{i}": f"r{i}" for i in range(len(pairs))}}
    return dict(
        key=key,
        type="MATCHING",
        section=section,
        mode="RECOGNITION",
        instructions=instructions,
        prompt={"left": left, "right": right},
        answer=answer,
        items=items,
        feedback=_fb(hint, expl),
        points=2,
    )


def build(key, section, instructions, sentence, items, hint, expl, extra_accepted=()):
    tiles = sentence.rstrip(".?!").split()
    return dict(
        key=key,
        type="SENTENCE_BUILDER",
        section=section,
        mode="RECALL",
        instructions=instructions,
        prompt={"tiles": tiles, "hint": hint},
        answer={"accepted": [sentence, *extra_accepted]},
        items=items,
        feedback=_fb(hint, expl),
        points=2,
    )


def blank(key, section, instructions, text, answers, word_bank, items, hint, expl, hint_ru=None):
    prompt: dict[str, Any] = {"text": text, "word_bank": word_bank}
    if hint_ru:
        prompt["hint_ru"] = hint_ru
    return dict(
        key=key,
        type="FILL_BLANK",
        section=section,
        mode="RECALL",
        instructions=instructions,
        prompt=prompt,
        answer={"blanks": [[a] for a in answers]},
        items=items,
        feedback=_fb(hint, expl),
        points=1,
    )


def order(key, section, instructions, events, items, hint, expl):
    prompt_items = [{"id": f"e{i}", "text": t} for i, t in enumerate(events)]
    return dict(
        key=key,
        type="ORDER_EVENTS",
        section=section,
        mode="RECOGNITION",
        instructions=instructions,
        prompt={"items": prompt_items},
        answer={"order": [f"e{i}" for i in range(len(events))]},
        items=items,
        feedback=_fb(hint, expl),
        points=2,
    )


def speak(key, instructions, text, model_answer, items):
    return dict(
        key=key,
        type="SPEAKING",
        section="SPEAKING",
        mode="RECALL",
        instructions=instructions,
        prompt={"text": text, "model_answer": model_answer},
        answer={},
        items=items,
        feedback={"correct": "Well done for speaking! Listen to the model and compare."},
        points=0,
    )
