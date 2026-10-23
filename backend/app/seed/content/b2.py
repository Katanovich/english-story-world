"""CEFR B2 · Upper-intermediate "Big Ideas" — 10 lessons in two units."""

from app.seed.content import b2_unit1, b2_unit2

ITEMS = {**b2_unit1.ITEMS, **b2_unit2.ITEMS}

LEVEL = {
    "cefr": "B2",
    "title": "B2 · Upper-intermediate",
    "description": "Big ideas: space, robots, climate, health, inventions, other cultures, travel and debate.",
    "units": [b2_unit1.UNIT, b2_unit2.UNIT],
}
