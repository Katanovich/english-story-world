"""CEFR B1 · Intermediate "Growing Up" — 10 lessons in two units."""

from app.seed.content import b1_unit1, b1_unit2

ITEMS = {**b1_unit1.ITEMS, **b1_unit2.ITEMS}

LEVEL = {
    "cefr": "B1",
    "title": "B1 · Intermediate",
    "description": "Growing up: clubs and friends, cooking, stories, rules, the environment and our town's past.",
    "units": [b1_unit1.UNIT, b1_unit2.UNIT],
}
