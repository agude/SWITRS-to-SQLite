#!/usr/bin/env python3

import pytest

from switrs_to_sqlite.make_map import MAKE_MAP, Make


def _make_values() -> set[str | None]:
    return {m.value for m in Make}


def test_all_values_are_make_enum_members() -> None:
    valid = _make_values()
    for key, value in MAKE_MAP.items():
        assert value in valid, f"MAKE_MAP[{key!r}] = {value!r} is not a Make enum value"


def test_keys_contain_no_dot_value() -> None:
    for key in MAKE_MAP:
        assert ".value" not in key, f"MAKE_MAP key {key!r} contains '.value' (enum access leak)"


def test_keys_are_uppercase_and_stripped() -> None:
    for key in MAKE_MAP:
        assert key == key.strip(), f"MAKE_MAP key {key!r} has leading/trailing whitespace"
        assert key == key.upper(), f"MAKE_MAP key {key!r} is not uppercase"


@pytest.mark.parametrize(
    ("raw_make", "expected_make"),
    [
        ("ODYSSEY", "honda"),
        ("RANGER", "ford"),
        ("PRIUS", "toyota"),
        ("RANGE RO", "land rover"),
        ("INTL", "international harvester"),
        ("TAOTA", "taotao"),
        ("TAOTAO", "taotao"),
        ("MASI", "maserati"),
        ("SUBN", "subaru"),
        ("MERC", "mercury"),
    ],
)
def test_documented_make_decisions_stay_pinned(raw_make: str, expected_make: str) -> None:
    assert MAKE_MAP[raw_make] == expected_make
