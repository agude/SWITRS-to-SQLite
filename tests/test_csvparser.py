#!/usr/bin/env python3

import pytest

from switrs_to_sqlite.converters import convert, string_to_bool
from switrs_to_sqlite.datatypes import DataType
from switrs_to_sqlite.parsers import CSVParser
from switrs_to_sqlite.schema import Column


@pytest.fixture(scope="module")
def row() -> list[str]:
    return ["9", "a", "1.", "Y"]


@pytest.fixture(scope="module")
def test_header() -> list[str]:
    return ["first", "second", "third", "forth", "blank"]


@pytest.fixture(scope="module")
def parsing_table() -> tuple[Column, ...]:
    return (
        Column(
            header="first", name="first", sql_type=DataType.INTEGER, converter=convert
        ),
        Column(
            header="second", name="second", sql_type=DataType.TEXT, converter=convert
        ),
        Column(header="third", name="third", sql_type=DataType.REAL, converter=convert),
        Column(
            header="forth",
            name="forth",
            sql_type=DataType.INTEGER,
            converter=string_to_bool,
        ),
        Column(
            header="blank",
            name="blank",
            sql_type=DataType.INTEGER,
            nulls=[""],
            converter=convert,
        ),
    )


@pytest.fixture(scope="function")
def parser(parsing_table: tuple[Column, ...], test_header: list[str]) -> CSVParser:
    Parser = CSVParser(
        parsing_table=parsing_table,
        table_name="Test",
        has_primary_column=False,
        date_parsing_table=None,
    )
    Parser.resolve_indices(test_header.copy())

    return Parser


def test_extend_row_without_has_primary_column(parser: CSVParser) -> None:
    parser.has_primary_column = False
    values = parser.parse_row([""])
    assert len(values) == 6


def test_extend_row_with_has_primary_column(parser: CSVParser) -> None:
    parser.has_primary_column = True
    values = parser.parse_row([""])
    assert len(values) == 5


def test_parse_row_without_has_primary_column(
    parser: CSVParser, row: list[str]
) -> None:
    parser.has_primary_column = False
    values = parser.parse_row(row)
    assert values == [None, 9, "a", 1.0, True, None]


def test_parse_row_with_has_primary_column(parser: CSVParser, row: list[str]) -> None:
    parser.has_primary_column = True
    values = parser.parse_row(row)
    assert values == [9, "a", 1.0, True, None]


def test_set_columns_without_has_primary_column(parser: CSVParser) -> None:
    assert parser.columns[0] == ("id", "INTEGER", "PRIMARY KEY")
    assert parser.columns[1] == ("first", "INTEGER")
    assert parser.columns[2] == ("second", "TEXT")
    assert parser.columns[3] == ("third", "REAL")
    assert parser.columns[4] == ("forth", "INTEGER")
    assert parser.columns[5] == ("blank", "INTEGER")


def test_set_columns_with_has_primary_column(parsing_table: tuple[Column, ...]) -> None:
    parser = CSVParser(
        parsing_table=parsing_table,
        table_name="Test",
        has_primary_column=True,
        date_parsing_table=None,
    )
    assert parser.columns[0] == ("first", "INTEGER", "PRIMARY KEY")
    assert parser.columns[1] == ("second", "TEXT")
    assert parser.columns[2] == ("third", "REAL")
    assert parser.columns[3] == ("forth", "INTEGER")
    assert parser.columns[4] == ("blank", "INTEGER")


def test_insert_statement(parser: CSVParser, row: list[str]) -> None:
    statement = parser.insert_statement(["?", "?", "?", "?", "?"])
    assert statement == "INSERT INTO Test VALUES (?, ?, ?, ?, ?)"


def test_create_table_statement_without_has_primary_column(parser: CSVParser) -> None:
    parser.has_primary_column = False
    statement = parser.create_table_statement()
    assert (
        statement
        == "CREATE TABLE Test (id INTEGER PRIMARY KEY, first INTEGER, second TEXT, third REAL, forth INTEGER, blank INTEGER)"
    )


def test_create_table_statement_with_has_primary_column(
    parsing_table: tuple[Column, ...],
) -> None:
    parser = CSVParser(
        parsing_table=parsing_table,
        table_name="Test",
        has_primary_column=True,
        date_parsing_table=None,
    )
    statement = parser.create_table_statement()
    assert (
        statement
        == "CREATE TABLE Test (first INTEGER PRIMARY KEY, second TEXT, third REAL, forth INTEGER, blank INTEGER)"
    )


def test_resolve_indices_raises_on_duplicate_headers(
    parsing_table: tuple[Column, ...],
) -> None:
    parser = CSVParser(
        parsing_table=parsing_table,
        table_name="Test",
        has_primary_column=False,
        date_parsing_table=None,
    )
    duplicate_header = [
        "first",
        "second",
        "third",
        "forth",
        "FIRST",
    ]  # FIRST duplicates first

    with pytest.raises(
        ValueError, match=r"Duplicate column header 'FIRST' at indices 0 and 4"
    ):
        parser.resolve_indices(duplicate_header)
