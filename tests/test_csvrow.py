#!/usr/bin/env python3

from load_into_database import CSVRow, DataType, convert, bool_yes_no
import pytest

@pytest.fixture(scope="module")
def csvrow():
    row = ["9", "a", "1.", "Y"]
    csvrow = CSVRow(row)
    csvrow.members = (
        (0, "first", DataType.INTEGER, None, convert),
        (1, "second", DataType.TEXT, None, convert),
        (2, "third", DataType.REAL, None, convert),
        (3, "forth", DataType.INTEGER, None, bool_yes_no),
        (4, "blank", DataType.INTEGER, (""), convert),
    )
    csvrow.extend_row()

    csvrow.table_name = "Test"

    return csvrow

def test_extend_row(csvrow):
    csvrow.extend_row()
    assert len(csvrow.row) == 5

def test_set_variables(csvrow):
    csvrow.set_variables()
    assert csvrow.first == 9
    assert csvrow.second == "a"
    assert csvrow.third == 1.
    assert csvrow.forth == True
    assert csvrow.blank == None

def test_set_values(csvrow):
    csvrow.set_variables()
    csvrow.set_values()
    assert csvrow.values[0] == 9
    assert csvrow.values[1] == "a"
    assert csvrow.values[2] == 1.
    assert csvrow.values[3] == True
    assert csvrow.values[4] == None

def test_set_columns(csvrow):
    csvrow.set_columns()
    assert csvrow.columns[0] == ("first", "INTEGER")
    assert csvrow.columns[1] == ("second", "TEXT")
    assert csvrow.columns[2] == ("third", "REAL")
    assert csvrow.columns[3] == ("forth", "INTEGER")
    assert csvrow.columns[4] == ("blank", "INTEGER")

def test_insert_statement(csvrow):
    csvrow.set_variables()
    csvrow.set_values()
    csvrow.set_columns()
    statement = csvrow.insert_statement()
    assert statement == "INSERT INTO Test VALUES (?, ?, ?, ?, ?)"

def test_create_table_statement(csvrow):
    csvrow.set_variables()
    csvrow.set_values()
    # Test without self.set_primary
    csvrow.set_columns()
    statement = csvrow.create_table_statement()
    assert statement == "CREATE TABLE Test (first INTEGER, second TEXT, third REAL, forth INTEGER, blank INTEGER)"
    # Test with self.set_primary
    csvrow.set_primary = True
    csvrow.set_columns()
    statement = csvrow.create_table_statement()
    assert statement == "CREATE TABLE Test (first INTEGER PRIMARY KEY, second TEXT, third REAL, forth INTEGER, blank INTEGER)"
