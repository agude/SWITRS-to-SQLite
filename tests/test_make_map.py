#!/usr/bin/env python3

import pytest

from switrs_to_sqlite.make_map import MAKE_MAP, Make


def _make_values() -> set[str | None]:
    return {m.value for m in Make}


def test_all_values_are_make_enum_members() -> None:
    valid = _make_values()
    for key, value in MAKE_MAP.items():
        assert value in valid, f"MAKE_MAP[{key!r}] = {value!r} is not a Make enum value"


@pytest.mark.xfail(
    reason="TREK.value key bug — fixed on dev-car_makes, ships in v5.0.0"
)
def test_keys_contain_no_dot_value() -> None:
    for key in MAKE_MAP:
        assert ".value" not in key, (
            f"MAKE_MAP key {key!r} contains '.value' (enum access leak)"
        )


@pytest.mark.xfail(
    reason="TREK.value key bug — fixed on dev-car_makes, ships in v5.0.0"
)
def test_keys_are_uppercase_and_stripped() -> None:
    for key in MAKE_MAP:
        assert key == key.strip(), (
            f"MAKE_MAP key {key!r} has leading/trailing whitespace"
        )
        assert key == key.upper(), f"MAKE_MAP key {key!r} is not uppercase"
