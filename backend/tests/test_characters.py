import json
import subprocess

import pytest

from app.seed import load_seed_data, validate_seed_data
from app.seed.characters import ROLES, load_names, personalize

FAMILY = {
    "boy": "Ivan",
    "little": "Olya",
    "teen": "Lena",
    "dad": "Pavel",
    "mum": "Vera",
    "gran1": "Galina",
    "gran2": "Nina",
    "aunt": "Irina",
}


def test_defaults_used_without_local_file(tmp_path):
    names = load_names(tmp_path / "missing.json")
    assert names == {role: default for role, (default, _) in ROLES.items()}


def test_local_file_overrides_names(tmp_path):
    f = tmp_path / "names.json"
    f.write_text(json.dumps(FAMILY))
    assert load_names(f)["boy"] == "Ivan"


@pytest.mark.parametrize(
    "bad", [{"boy": "Mir ko"}, {"boy": "мирко"}, {"villain": "X"}, {"boy": ""}]
)
def test_invalid_names_rejected(tmp_path, bad):
    f = tmp_path / "names.json"
    f.write_text(json.dumps(bad))
    with pytest.raises(ValueError):
        load_names(f)


def test_personalize_replaces_every_placeholder():
    data = load_seed_data(FAMILY)
    validate_seed_data(data)  # sentence-building tiles stay valid with the new names
    blob = json.dumps([data.course, data.levels, data.items], ensure_ascii=False)
    for role in ROLES:
        assert "{" + role + "}" not in blob
    assert "Ivan" in blob and "Galina" in blob and "Irina" in blob
    assert personalize({"a": ["{boy} & {little}"]}, FAMILY) == {"a": ["Ivan & Olya"]}


def test_local_names_file_is_git_ignored():
    result = subprocess.run(  # noqa: S603
        ["git", "check-ignore", "-q", "app/seed/characters.local.json"],  # noqa: S607
        check=False,
    )
    assert result.returncode == 0
