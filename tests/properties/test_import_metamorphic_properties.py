"""Transformations of the input files that must not change the database."""

import contextlib
import sqlite3
import tempfile
from dataclasses import dataclass
from pathlib import Path

from conftest import COLLISION_HEADER, PARTY_HEADER, VICTIM_HEADER
from hypothesis import event, given, settings
from hypothesis import strategies as st
from import_helpers import write_csv

from switrs_to_sqlite.main import convert_files

Records = list[dict[str, str]]

UNKNOWN_COLUMN = "UNUSED_COLUMN"
FIELD_VALUES = (
    "",
    "-",
    " ",
    "0",
    "1",
    "2",
    "A",
    "B",
    "F",
    "N",
    "Y",
    " 3 ",
    "12.5",
    "0930",
    "2500",
    "20200229",
    'Road, "Main"',
    "Café",
)
TABLE_HEADERS = {
    "collisions": COLLISION_HEADER,
    "parties": PARTY_HEADER,
    "victims": VICTIM_HEADER,
}


@dataclass(frozen=True)
class InputFormat:
    """How one import lays out the same records on disk."""

    compressed: bool = False
    reverse_headers: bool = False
    has_unknown_column: bool = False
    has_blank_lines: bool = False


def records_for(headers: list[str]) -> st.SearchStrategy[Records]:
    """Generate rows that share a small case ID pool and field vocabulary."""
    case_ids = st.integers(min_value=1, max_value=3).map(str)
    fields = st.lists(
        st.sampled_from(FIELD_VALUES), min_size=len(headers) - 1, max_size=len(headers) - 1
    )
    record = st.builds(
        lambda case_id, values: dict(zip(headers, [case_id, *values], strict=True)),
        case_ids,
        fields,
    )
    return st.lists(record, max_size=4)


def import_dump(tables: dict[str, Records], input_format: InputFormat) -> list[str]:
    """Import the records in the given layout and return the database dump."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory)
        input_paths: dict[str, str] = {}
        for table, table_headers in TABLE_HEADERS.items():
            headers = list(table_headers)
            records = tables[table]
            if input_format.has_unknown_column:
                headers.append(UNKNOWN_COLUMN)
                records = [{**record, UNKNOWN_COLUMN: "ignored"} for record in records]
            if input_format.reverse_headers:
                headers.reverse()
            path = directory / f"{table}.csv"
            write_csv(
                path,
                headers,
                records,
                compressed=input_format.compressed,
                has_blank_lines=input_format.has_blank_lines,
            )
            input_paths[table] = str(path)

        database = directory / "output.sqlite3"
        convert_files(
            input_paths["collisions"],
            input_paths["parties"],
            input_paths["victims"],
            str(database),
        )
        with contextlib.closing(sqlite3.connect(database)) as connection:
            return list(connection.iterdump())


@settings(deadline=None)
@given(
    tables=st.fixed_dictionaries(
        {table: records_for(headers) for table, headers in TABLE_HEADERS.items()}
    ),
    input_format=st.sampled_from(
        [
            InputFormat(compressed=True),
            InputFormat(reverse_headers=True),
            InputFormat(has_unknown_column=True),
            InputFormat(has_blank_lines=True),
            InputFormat(compressed=True, reverse_headers=True, has_unknown_column=True),
        ]
    ),
)
def test_input_layout_does_not_change_the_database(
    tables: dict[str, Records], input_format: InputFormat
) -> None:
    collision_ids = [record["CASE_ID"] for record in tables["collisions"]]
    event(f"duplicate collision IDs: {len(collision_ids) != len(set(collision_ids))}")
    event(f"total rows: {sum(len(records) for records in tables.values())}")

    assert import_dump(tables, input_format) == import_dump(tables, InputFormat())
