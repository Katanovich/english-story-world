"""CEFR C2 · Proficiency "Mastery" — 10 lessons in two units."""

from app.seed.content import c2_unit1, c2_unit2

ITEMS = {**c2_unit1.ITEMS, **c2_unit2.ITEMS}

LEVEL = {
    "cefr": "C2",
    "title": "C2 · Proficiency",
    "description": "Mastery: idioms, literature, humour, academic writing, debate, translation, diplomacy, poetry and the family film.",
    "units": [c2_unit1.UNIT, c2_unit2.UNIT],
}
