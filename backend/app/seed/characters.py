"""Story characters.

Lesson content uses placeholders such as {boy} or {gran1}. The public repository ships
neutral default names; a family can use its own names by creating the git-ignored file
`backend/app/seed/characters.local.json`, e.g.:

    {"boy": "Ivan", "little": "Olya", "teen": "Lena", "dad": "Pavel", "mum": "Vera",
     "gran1": "Galina", "gran2": "Nina", "aunt": "Irina"}

and then running `python -m app.cli seed --update`.
"""

import json
import re
from pathlib import Path
from typing import Any

# role -> (default name, description)
ROLES: dict[str, tuple[str, str]] = {
    "boy": ("Alex", "the main hero, a boy of about 9"),
    "little": ("Mia", "his little sister, 5 years old"),
    "teen": ("Kate", "his older sister, a teenager"),
    "dad": ("Tom", "father"),
    "mum": ("Anna", "mother"),
    "gran1": ("Rose", "first grandmother"),
    "gran2": ("Lily", "second grandmother"),
    "aunt": ("Emma", "aunt"),
}

LOCAL_FILE = Path(__file__).with_name("characters.local.json")
_TOKEN = re.compile(r"\{(" + "|".join(ROLES) + r")\}")
_NAME = re.compile(r"^[A-Z][A-Za-z\-]{0,30}$")


def load_names(path: Path = LOCAL_FILE) -> dict[str, str]:
    names = {role: default for role, (default, _) in ROLES.items()}
    if path.exists():
        custom = json.loads(path.read_text(encoding="utf-8"))
        for role, name in custom.items():
            if role not in ROLES:
                raise ValueError(f"Unknown character role '{role}' in {path.name}")
            # One capitalised Latin word, so sentence-building tiles stay valid.
            if not isinstance(name, str) or not _NAME.match(name):
                raise ValueError(
                    f"Name for '{role}' must be one word in Latin letters, got {name!r}"
                )
            names[role] = name
    return names


def personalize(value: Any, names: dict[str, str]) -> Any:
    """Recursively replace {role} placeholders in every string."""
    if isinstance(value, str):
        return _TOKEN.sub(lambda m: names[m.group(1)], value)
    if isinstance(value, list):
        return [personalize(v, names) for v in value]
    if isinstance(value, tuple):
        return tuple(personalize(v, names) for v in value)
    if isinstance(value, dict):
        return {k: personalize(v, names) for k, v in value.items()}
    return value
