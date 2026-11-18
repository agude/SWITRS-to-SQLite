"""Model-based properties for CSVParser's small synthetic schemas."""

import math
from collections.abc import Sequence

import pytest
from hypothesis import event, example, given
from hypothesis import strategies as st

from switrs_to_sqlite.converters import convert
from switrs_to_sqlite.datatypes import DataType
from switrs_to_sqlite.parsers import CSVParser
from switrs_to_sqlite.schema import Column

FIELDS = ("record_id", "label", "amount")
MAPPING = {"alpha": "A", "beta": "B"}


def make_columns() -> tuple[Column, ...]:
    return (
        Column("RECORD_ID", "record_id", DataType.INTEGER, converter=convert),
        Column("label", "label", DataType.TEXT, converter=convert, mapping=MAPPING),
        Column("amount", "amount", DataType.REAL, converter=convert),
    )


def make_parser(has_primary_column: bool = True) -> CSVParser:
    return CSVParser(make_columns(), "records", has_primary_column)


def model_number(number_type: type[int] | type[float], text: str) -> int | float | None:
    """Reference parsing: plain, finite, ASCII numbers only."""
    if not text.isascii() or "_" in text:
        return None
    try:
        number = number_type(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def model_value(header: str, raw: str) -> object:
    """Reference conversion for the deliberately small schema above."""
    stripped = raw.strip()
    if header == "record_id":
        return model_number(int, stripped)
    if header == "amount":
        return model_number(float, stripped)
    return MAPPING.get(stripped, stripped)


def header_row(order: Sequence[str]) -> list[str]:
    return [name.upper() if index % 2 else name for index, name in enumerate(order)]


@given(
    order=st.permutations(FIELDS),
    record_id=st.integers(min_value=-100_000, max_value=100_000).map(str),
    label=st.sampled_from(["alpha", "beta", "gamma", "  text  "]),
    amount=st.floats(allow_nan=False, allow_infinity=False, width=32).map(str),
    has_primary_column=st.booleans(),
    unknown_position=st.integers(0, len(FIELDS)),
    unknown_value=st.text(max_size=8),
)
def test_parser_matches_dictionary_model_for_reordered_headers(
    order: list[str],
    record_id: str,
    label: str,
    amount: str,
    has_primary_column: bool,
    unknown_position: int,
    unknown_value: str,
) -> None:
    headers = order.copy()
    headers.insert(unknown_position, "ignored_field")
    raw_values = {
        "record_id": record_id,
        "label": label,
        "amount": amount,
        "ignored_field": unknown_value,
    }
    parser = make_parser(has_primary_column)
    parser.resolve_indices(header_row(headers))

    actual = parser.parse_row([raw_values[name] for name in headers])
    expected = [model_value(field, raw_values[field]) for field in FIELDS]
    if not has_primary_column:
        expected.insert(0, None)

    assert actual == expected


@given(order=st.permutations(FIELDS))
def test_re_resolving_headers_replaces_the_previous_mapping(
    order: list[str],
) -> None:
    parser = make_parser()
    parser.resolve_indices(list(FIELDS))
    parser.resolve_indices(list(order))
    values = {"record_id": "17", "label": "alpha", "amount": "2.5"}

    assert parser.parse_row([values[field] for field in order]) == [17, "A", 2.5]


@given(order=st.permutations(FIELDS), prefix=st.lists(st.text(max_size=5), max_size=2))
@example(order=["record_id", "amount", "label"], prefix=["", "NAN"])
def test_short_rows_pad_missing_trailing_columns_with_empty_values(
    order: list[str], prefix: list[str]
) -> None:
    parser = make_parser()
    parser.resolve_indices(list(order))
    event(f"fields present: {len(prefix)}")
    raw_values = dict(zip(order[: len(prefix)], prefix, strict=True))
    expected = [model_value(field, raw_values.get(field, "")) for field in FIELDS]

    assert parser.parse_row(prefix) == expected


@given(header=st.sampled_from(FIELDS))
def test_missing_required_header_is_rejected(header: str) -> None:
    parser = make_parser()
    incomplete_header = [field for field in FIELDS if field != header]

    with pytest.raises(ValueError, match=f"Missing expected column: {header}"):
        parser.resolve_indices(incomplete_header)


@given(header=st.sampled_from(FIELDS), case=st.sampled_from(["lower", "upper"]))
def test_duplicate_headers_are_rejected_case_insensitively(header: str, case: str) -> None:
    parser = make_parser()
    duplicate = header.upper() if case == "upper" else header

    with pytest.raises(ValueError, match="Duplicate column header"):
        parser.resolve_indices([*FIELDS, duplicate])


@given(has_primary_column=st.booleans())
def test_sql_columns_parameters_and_key_shape_follow_schema_order(
    has_primary_column: bool,
) -> None:
    parser = make_parser(has_primary_column)
    parser.resolve_indices(list(FIELDS))
    expected_columns = list(FIELDS)
    if not has_primary_column:
        expected_columns.insert(0, "id")
    parameter_columns = parser.insert_statement().split("(", 1)[1].split(")", 1)[0]
    placeholders = parser.insert_statement().split("VALUES (", 1)[1].rstrip(")").split(", ")

    assert [column[0] for column in parser.columns] == expected_columns
    assert parameter_columns.split(", ") == expected_columns
    assert placeholders == ["?"] * len(expected_columns)
    insert_prefix = "INSERT OR IGNORE" if has_primary_column else "INSERT"
    assert parser.insert_statement().partition(" INTO ")[0] == insert_prefix
    assert parser.columns[0][-1] == "PRIMARY KEY"
    assert parser.parse_row(["1", "gamma", "2.0"]) == (
        [1, "gamma", 2.0] if has_primary_column else [None, 1, "gamma", 2.0]
    )
