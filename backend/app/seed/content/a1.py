"""CEFR A1 · Beginner — 10 lessons in two units."""

from app.seed.content import a1_unit1, a1_unit2

ITEMS = {**a1_unit1.ITEMS, **a1_unit2.ITEMS}

LEVEL = {
    "cefr": "A1",
    "title": "A1 · Beginner",
    "description": "First words and sentences: family, home, pets, toys, food, weather.",
    "units": [a1_unit1.UNIT, a1_unit2.UNIT],
}
