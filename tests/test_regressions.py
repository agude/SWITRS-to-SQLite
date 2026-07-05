#!/usr/bin/env python3
"""Regression tests for bugs identified in plan.md, section 1."""

from pathlib import Path

import pytest
from conftest import (
    COLLISION_HEADER,
    COLLISIONS_HEADER_CSV,
    PARTIES_HEADER_CSV,
    VICTIMS_HEADER_CSV,
)

from switrs_to_sqlite.converters import negative
from switrs_to_sqlite.main import main
from switrs_to_sqlite.parsers import CSVParser

DATA_DIR = Path(__file__).parent / "data"

# Output rows from CollisionRow end with the three derived date columns,
# in this order: collision_date, collision_time, process_date.
COLLISION_DATE_IDX = -3
COLLISION_TIME_IDX = -2
PROCESS_DATE_IDX = -1


def make_collision_row(**fields: str) -> list[str]:
    """Build a blank collision CSV row, overriding the given header fields."""
    row = [""] * len(COLLISION_HEADER)
    for header, value in fields.items():
        row[COLLISION_HEADER.index(header)] = value
    return row


def test_empty_dates_become_null(collision_parser: CSVParser) -> None:
    row = make_collision_row(CASE_ID="CASE1")
    values = collision_parser.parse_row(row)
    assert values[COLLISION_DATE_IDX] is None
    assert values[PROCESS_DATE_IDX] is None


def test_malformed_dates_become_null(collision_parser: CSVParser) -> None:
    row = make_collision_row(
        CASE_ID="CASE1",
        COLLISION_DATE="not-a-date",
        PROC_DATE="2020011",  # Too short for %Y%m%d
    )
    values = collision_parser.parse_row(row)
    assert values[COLLISION_DATE_IDX] is None
    assert values[PROCESS_DATE_IDX] is None


def test_short_row_parses_with_null_dates(collision_parser: CSVParser) -> None:
    values = collision_parser.parse_row(["CASE1", "2020", "20200101"])
    assert values[COLLISION_DATE_IDX] is None
    assert values[COLLISION_TIME_IDX] is None


def test_malformed_collision_time_becomes_null(collision_parser: CSVParser) -> None:
    row = make_collision_row(
        CASE_ID="CASE1",
        COLLISION_DATE="20200101",
        PROC_DATE="20200416",
        COLLISION_TIME="9999",
    )
    values = collision_parser.parse_row(row)
    assert values[COLLISION_DATE_IDX] == "2020-01-01"
    assert values[COLLISION_TIME_IDX] is None
    assert values[PROCESS_DATE_IDX] == "2020-04-16"


def test_negative_preserves_already_negative_values() -> None:
    # The raw data ships positive longitudes with implied west, but a
    # signed input must not silently flip to the eastern hemisphere.
    assert negative("-121.5", float, None) == -121.5
    # The documented behavior for unsigned input must not change.
    assert negative("121.5", float, None) == -121.5


def test_rerun_on_existing_database_fails_cleanly(tmp_path: Path) -> None:
    # A second run against the same output file must fail with a clear
    # CLI error, not an unhandled OperationalError mid-run. If the fix
    # adds overwrite semantics (e.g. --force), update this contract.
    collisions_path = tmp_path / "collisions.txt"
    parties_path = tmp_path / "parties.txt"
    victims_path = tmp_path / "victims.txt"
    db_path = tmp_path / "switrs.sqlite3"

    collisions_path.write_text(
        COLLISIONS_HEADER_CSV + "\n" + (DATA_DIR / "test_collisions.txt").read_text()
    )
    parties_path.write_text(
        PARTIES_HEADER_CSV + "\n" + (DATA_DIR / "test_parties.txt").read_text()
    )
    victims_path.write_text(
        VICTIMS_HEADER_CSV + "\n" + (DATA_DIR / "test_victims.txt").read_text()
    )

    args = [
        str(collisions_path),
        str(parties_path),
        str(victims_path),
        "-o",
        str(db_path),
    ]
    main(args)
    with pytest.raises(SystemExit):
        main(args)
