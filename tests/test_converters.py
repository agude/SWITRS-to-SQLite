#!/usr/bin/env python3

from switrs_to_sqlite.converters import (
    cellphone_use_to_bool,
    convert,
    county_city_location_to_county,
    negative,
    non_standard_str_to_bool,
    string_to_bool,
)


# Test the convert function
def test_convert() -> None:
    convert_vals = (
        # Pass through
        ("9", None, None, "9"),
        ("a", None, None, "a"),
        ("1.", None, None, "1."),
        # Standard dtypes
        ("9", int, None, 9),
        ("a", str, None, "a"),
        ("1", float, None, 1.0),
        # With spaces
        ("9 ", int, None, 9),
        ("a ", str, None, "a"),
        ("1 ", float, None, 1.0),
        (" 9", int, None, 9),
        (" a", str, None, "a"),
        (" 1", float, None, 1.0),
        # Nulls that do nothing
        ("9", int, [""], 9),
        ("a", str, [""], "a"),
        ("1", float, [""], 1.0),
        # Nulls that return None
        ("9", int, ["9"], None),
        ("a", str, ["a"], None),
        ("1.", float, ["1."], None),
        ("9", None, ["9"], None),
        ("a", None, ["a"], None),
        ("1.", None, ["1."], None),
        # Conversion failure
        ("a", int, None, None),
    )
    for val, dtype, nulls, res in convert_vals:
        assert convert(val, dtype, nulls) == res


# Test the negative function
def test_negative() -> None:
    convert_vals = (
        # Pass through (no dtype) returns None since strings can't be negated
        ("9", None, None, None),
        ("a", None, None, None),
        ("1.", None, None, None),
        # Standard numeric dtypes
        ("9", int, None, -9),
        ("1", float, None, -1.0),
        # String dtype returns None since strings can't be negated
        ("a", str, None, None),
        # With spaces
        ("9 ", int, None, -9),
        ("1 ", float, None, -1.0),
        (" 9", int, None, -9),
        (" 1", float, None, -1.0),
        # String with spaces returns None
        ("a ", str, None, None),
        (" a", str, None, None),
        # Nulls that do nothing
        ("9", int, [""], -9),
        ("1", float, [""], -1.0),
        # Nulls that return None
        ("9", int, ["9"], None),
        ("1.", float, ["1."], None),
        ("9", None, ["9"], None),
        ("a", None, ["a"], None),
        ("1.", None, ["1."], None),
        # Conversion failure
        ("a", int, None, None),
    )
    for val, dtype, nulls, res in convert_vals:
        assert negative(val, dtype, nulls) == res


# Test the string_to_bool function
def test_bools() -> None:
    bools = (
        ("Y", True),
        ("y", True),
        ("N", False),
        ("n", False),
    )
    for val, res in bools:
        assert string_to_bool(val) == res


def test_nulls() -> None:
    nones = (
        ("Y", ["Y"]),
        ("y", ["y"]),
        ("N", ["N"]),
        ("n", ["n"]),
        ("", [""]),
        ("1", ["1"]),
    )
    for val, nulls in nones:
        assert string_to_bool(val, None, nulls) is None


def test_county_city_location_to_county() -> None:
    convert_vals = (
        ("0145", str, None, "01"),
        ("5899", str, None, "58"),
        # Nulls that return None
        ("9", int, ["9"], None),
        ("a", str, ["a"], None),
        ("1.", float, ["1."], None),
        ("9", None, ["9"], None),
        ("a", None, ["a"], None),
        ("1.", None, ["1."], None),
        # Conversion failure
        ("a", int, None, None),
    )
    for val, dtype, nulls, res in convert_vals:
        assert county_city_location_to_county(val, dtype, nulls) == res


def test_cellphone_use_to_bool() -> None:
    convert_vals = (
        ("B", int, None, True),
        ("C", int, None, False),
        ("D", int, None, None),
        ("1", int, None, True),
        ("2", int, None, True),
        ("3", int, None, False),
        # Nulls that return None
        ("9", int, ["9"], None),
        ("a", str, ["a"], None),
        ("1.", float, ["1."], None),
        ("9", None, ["9"], None),
        ("a", None, ["a"], None),
        ("1.", None, ["1."], None),
        # Conversion failure
        ("a", int, None, None),
    )
    for val, dtype, nulls, res in convert_vals:
        assert cellphone_use_to_bool(val, dtype, nulls) == res


def test_non_standard_str_to_bool() -> None:
    convert_vals = (
        ("A", int, None, True),
        ("E", int, None, True),
        # Unknown keys
        ("D", int, None, None),
        ("1", int, None, None),
        ("2", int, None, None),
        ("3", int, None, None),
        # Nulls that return None
        ("9", int, ["9"], None),
        ("a", str, ["a"], None),
        ("1.", float, ["1."], None),
        ("9", None, ["9"], None),
        ("a", None, ["a"], None),
        ("1.", None, ["1."], None),
        # Conversion failure
        ("a", int, None, None),
    )
    for val, dtype, nulls, res in convert_vals:
        assert non_standard_str_to_bool(val, dtype, nulls) == res
