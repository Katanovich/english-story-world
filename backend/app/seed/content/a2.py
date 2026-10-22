"""CEFR A2 · Elementary "Everyday Adventures" — 10 lessons in two units."""

from app.seed.content import a2_unit1, a2_unit2

ITEMS = {**a2_unit1.ITEMS, **a2_unit2.ITEMS}

LEVEL = {
    "cefr": "A2",
    "title": "A2 · Elementary",
    "description": "Everyday adventures: school, daily routines, shopping, a family trip and the past.",
    "units": [a2_unit1.UNIT, a2_unit2.UNIT],
}
