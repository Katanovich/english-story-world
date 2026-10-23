"""All seed curriculum content, level by level (see COURSE_PLAN.md for the full plan)."""

from app.seed.content import a1, a2, b1, b2, c1, c2

COURSE = {
    "slug": "english-story-world",
    "title": "English Story World",
    "description": "Learn English with {boy}, {little} and their family through stories and games.",
}

# Levels in course order (A1 → C2).
LEVEL_MODULES = [a1, a2, b1, b2, c1, c2]

LEVELS = [m.LEVEL for m in LEVEL_MODULES]

ITEMS: dict = {}
for _m in LEVEL_MODULES:
    _dupes = set(ITEMS) & set(_m.ITEMS)
    if _dupes:
        raise ValueError(f"Duplicate learning item keys: {sorted(_dupes)}")
    ITEMS.update(_m.ITEMS)
