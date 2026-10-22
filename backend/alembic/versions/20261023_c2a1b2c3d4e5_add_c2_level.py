"""add C2 CEFR level

Revision ID: c2a1b2c3d4e5
Revises: 9ff97c1edaac
Create Date: 2026-10-23
"""

from alembic import op

revision = "c2a1b2c3d4e5"
down_revision = "9ff97c1edaac"
branch_labels = None
depends_on = None

# (table, column) pairs that use the cefr_level enum (VARCHAR + CHECK constraint).
COLUMNS = [
    ("course_levels", "cefr_level"),
    ("lessons", "cefr_level"),
    ("enrollments", "current_level"),
    ("learning_items", "cefr_level"),
]


def _replace(levels: list[str]) -> None:
    values = ", ".join(f"'{v}'" for v in levels)
    for table, column in COLUMNS:
        op.drop_constraint(op.f(f"ck_{table}_cefr_level"), table, type_="check")
        op.create_check_constraint("cefr_level", table, f"{column} IN ({values})")


def upgrade() -> None:
    _replace(["A1", "A2", "B1", "B2", "C1", "C2"])


def downgrade() -> None:
    _replace(["A1", "A2", "B1", "B2", "C1"])
