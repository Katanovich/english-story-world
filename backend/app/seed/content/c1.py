"""CEFR C1 · Advanced "Making a Difference" — 10 lessons in two units."""

from app.seed.content import c1_unit1, c1_unit2

ITEMS = {**c1_unit1.ITEMS, **c1_unit2.ITEMS}

LEVEL = {
    "cefr": "C1",
    "title": "C1 · Advanced",
    "description": "Making a difference: media, fake news, sustainability, creative writing, memoirs, AI and presenting.",
    "units": [c1_unit1.UNIT, c1_unit2.UNIT],
}
