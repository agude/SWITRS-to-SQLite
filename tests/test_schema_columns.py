"""Hand-written expectations for the real table declarations.

These values are deliberately not derived from row_types.py, so a wrong
declaration cannot change the expected result along with the code.
"""

from collections.abc import Callable
from dataclasses import dataclass

import pytest
from conftest import COLLISION_HEADER, PARTY_HEADER, VICTIM_HEADER

from switrs_to_sqlite.datatypes import DATATYPE_MAP
from switrs_to_sqlite.parsers import (
    CSVParser,
    make_collision_parser,
    make_party_parser,
    make_victim_parser,
)
from switrs_to_sqlite.row_types import COLLISION_ROW, PARTY_ROW, VICTIM_ROW
from switrs_to_sqlite.schema import Column


@dataclass(frozen=True)
class TextColumn:
    """Expected parsing of one TEXT column."""

    make_parser: Callable[[], CSVParser]
    headers: list[str]
    header: str
    column: str
    padded: str
    padded_result: str


NULLABLE_TEXT_COLUMNS = [
    TextColumn(make_collision_parser, COLLISION_HEADER, "OFFICER_ID", "officer_id", " 7 ", "7"),
    TextColumn(
        make_collision_parser, COLLISION_HEADER, "CHP_SHIFT", "chp_shift", " 1 ", "0600 thru 1359"
    ),
    TextColumn(make_collision_parser, COLLISION_HEADER, "PRIMARY_RD", "primary_road", " A ", "A"),
    TextColumn(
        make_collision_parser, COLLISION_HEADER, "SECONDARY_RD", "secondary_road", " B ", "B"
    ),
    TextColumn(
        make_collision_parser,
        COLLISION_HEADER,
        "COLLISION_SEVERITY",
        "collision_severity",
        " 1 ",
        "fatal",
    ),
    TextColumn(
        make_collision_parser, COLLISION_HEADER, "HIT_AND_RUN", "hit_and_run", " F ", "felony"
    ),
    TextColumn(make_party_parser, PARTY_HEADER, "CASE_ID", "case_id", " 9 ", "9"),
    TextColumn(make_victim_parser, VICTIM_HEADER, "CASE_ID", "case_id", " 9 ", "9"),
    TextColumn(make_victim_parser, VICTIM_HEADER, "VICTIM_ROLE", "victim_role", " 1 ", "driver"),
    TextColumn(
        make_victim_parser,
        VICTIM_HEADER,
        "VICTIM_SEATING_POSITION",
        "victim_seating_position",
        " 1 ",
        "driver",
    ),
]


def parse_field(text_column: TextColumn, raw_value: str) -> object:
    """Parse a row where only one field is populated."""
    parser = text_column.make_parser()
    parser.resolve_indices(text_column.headers.copy())
    row = [""] * len(text_column.headers)
    row[text_column.headers.index(text_column.header)] = raw_value
    column_names = [column[0] for column in parser.columns]
    return parser.parse_row(row)[column_names.index(text_column.column)]


@pytest.mark.parametrize("text_column", NULLABLE_TEXT_COLUMNS, ids=lambda item: item.column)
@pytest.mark.parametrize("null_token", ["", "-", "  ", " - "])
def test_text_column_null_tokens_become_null(text_column: TextColumn, null_token: str) -> None:
    assert parse_field(text_column, null_token) is None


@pytest.mark.parametrize("text_column", NULLABLE_TEXT_COLUMNS, ids=lambda item: item.column)
def test_text_column_strips_whitespace_before_mapping(text_column: TextColumn) -> None:
    assert parse_field(text_column, text_column.padded) == text_column.padded_result


COLLISION_CASE_ID = TextColumn(
    make_collision_parser, COLLISION_HEADER, "CASE_ID", "case_id", " 9 ", "9"
)


@pytest.mark.parametrize(("raw_value", "expected"), [("", ""), ("-", "-"), (" 9 ", "9")])
def test_collision_case_id_is_never_null(raw_value: str, expected: str) -> None:
    assert parse_field(COLLISION_CASE_ID, raw_value) == expected


MAPPED_COLUMNS = [
    column for row in (COLLISION_ROW, PARTY_ROW, VICTIM_ROW) for column in row if column.mapping
]


@pytest.mark.parametrize("column", MAPPED_COLUMNS, ids=lambda item: item.name)
def test_every_mapping_key_is_reachable(column: Column) -> None:
    """The converter must be able to produce each key the mapping defines."""
    assert column.mapping is not None
    dtype = DATATYPE_MAP[column.sql_type]
    unreachable_keys = [
        key for key in column.mapping if column.converter(key, dtype, column.nulls) != key
    ]
    assert unreachable_keys == []
