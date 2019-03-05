#!/usr/bin/env python3

from switrs_to_sqlite.converters import convert, string_to_bool
from switrs_to_sqlite.datatypes import DataType
from switrs_to_sqlite.parsers import CSVParser

import pytest


@pytest.fixture(scope="module")
def row():
    return ["9", "a", "1.", "Y"]

@pytest.fixture(scope="module")
def parsing_table():
    return (
        (0, "first", DataType.INTEGER, None, convert, None),
        (1, "second", DataType.TEXT, None, convert, None),
        (2, "third", DataType.REAL, None, convert, None),
        (3, "forth", DataType.INTEGER, None, string_to_bool, None),
        (4, "blank", DataType.INTEGER, (""), convert, None),
    )

@pytest.fixture(scope="function")
def parser(parsing_table):
    Parser = CSVParser(
        parsing_table=parsing_table,
        table_name="Test",
        has_primary_column=False,
        date_parsing_table=None,
    )

    return Parser


def test_extend_row_without_has_primary_column(parser):
    parser.has_primary_column = False
    values = parser.parse_row([""])
    assert len(values) == 6


def test_extend_row_with_has_primary_column(parser):
    parser.has_primary_column = True
    values = parser.parse_row([""])
    assert len(values) == 5


def test_parse_row_without_has_primary_column(parser, row):
    parser.has_primary_column = False
    values = parser.parse_row(row)
    assert values == [None, 9, "a", 1., True, None]


def test_parse_row_with_has_primary_column(parser, row):
    parser.has_primary_column = True
    values = parser.parse_row(row)
    assert values == [9, "a", 1., True, None]


def test_set_columns_without_has_primary_column(parser):
    assert parser.columns[0] == ("id", "INTEGER", "PRIMARY KEY")
    assert parser.columns[1] == ("first", "INTEGER")
    assert parser.columns[2] == ("second", "TEXT")
    assert parser.columns[3] == ("third", "REAL")
    assert parser.columns[4] == ("forth", "INTEGER")
    assert parser.columns[5] == ("blank", "INTEGER")


def test_set_columns_with_has_primary_column(parsing_table):
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


def test_insert_statement(parser, row):
    statement = parser.insert_statement(['?', '?', '?', '?', '?'])
    assert statement == "INSERT INTO Test VALUES (?, ?, ?, ?, ?)"


def test_create_table_statement_without_has_primary_column(parser):
    parser.has_primary_column = False
    statement = parser.create_table_statement()
    assert statement == "CREATE TABLE Test (id INTEGER PRIMARY KEY, first INTEGER, second TEXT, third REAL, forth INTEGER, blank INTEGER)"


def test_create_table_statement_with_has_primary_column(parsing_table):
    parser = CSVParser(
        parsing_table=parsing_table,
        table_name="Test",
        has_primary_column=True,
        date_parsing_table=None,
    )
    statement = parser.create_table_statement()
    assert statement == "CREATE TABLE Test (first INTEGER PRIMARY KEY, second TEXT, third REAL, forth INTEGER, blank INTEGER)"
