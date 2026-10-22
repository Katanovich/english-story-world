"""Management commands.

python -m app.cli create-admin      # uses ADMIN_EMAIL / ADMIN_USERNAME / ADMIN_PASSWORD
python -m app.cli seed              # curriculum content; safe to rerun
python -m app.cli seed --update     # re-apply seed content over existing records
"""

import argparse
import sys

from app.core.config import get_settings
from app.core.security import hash_password, password_problem
from app.db.session import SessionLocal
from app.models import User
from app.models.enums import AccountStatus, UserRole
from app.services import audit
from app.services.auth import find_user_by_login

WEAK_PASSWORDS = {"admin", "password", "changeme", "change-me", "admin123", "password123"}


class CommandError(Exception):
    pass


def create_admin(email: str | None, username: str | None, password: str | None) -> str:
    """Create the initial administrator. Safe to rerun: an existing account is left unchanged."""
    if not username or not password:
        raise CommandError("ADMIN_USERNAME and ADMIN_PASSWORD must be set.")
    problem = password_problem(password)
    if problem or password.lower() in WEAK_PASSWORDS or len(password) < 12:
        raise CommandError("Admin password is too weak: use at least 12 characters, mixed.")
    username = username.strip().lower()
    with SessionLocal() as db:
        existing = find_user_by_login(db, username) or (
            find_user_by_login(db, email) if email else None
        )
        if existing:
            if existing.role != UserRole.ADMIN:
                raise CommandError("A non-admin user with this username or email already exists.")
            return f"Admin '{existing.username}' already exists; nothing changed."
        user = User(
            username=username,
            email=email.strip().lower() if email else None,
            display_name="Administrator",
            password_hash=hash_password(password),
            role=UserRole.ADMIN,
            status=AccountStatus.ACTIVE,
        )
        db.add(user)
        db.flush()
        audit.record(db, None, "admin.bootstrap", "user", user.id)
        db.commit()
        return f"Admin '{username}' created."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("create-admin", help="Create the initial admin from environment variables")
    seed = sub.add_parser("seed", help="Create the A1 'Little Explorers' curriculum")
    seed.add_argument("--update", action="store_true", help="Overwrite existing seed records")
    args = parser.parse_args(argv)

    if args.command == "create-admin":
        s = get_settings()
        try:
            print(create_admin(s.admin_email, s.admin_username, s.admin_password))
        except CommandError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    elif args.command == "seed":
        from app.seed import run_seed

        with SessionLocal() as db:
            print("Seed " + run_seed(db, update=args.update).summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
