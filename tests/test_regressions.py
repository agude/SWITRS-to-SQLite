#!/usr/bin/env python3
"""Regression tests for legacy record conversion and CLI behavior."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from conftest import (
    COLLISION_HEADER,
    COLLISIONS_HEADER_CSV,
    PARTIES_HEADER_CSV,
    VICTIMS_HEADER_CSV,
)

from switrs_to_sqlite import __version__
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


def test_rerun_on_existing_database_fails_cleanly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
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
    parties_path.write_text(PARTIES_HEADER_CSV + "\n" + (DATA_DIR / "test_parties.txt").read_text())
    victims_path.write_text(VICTIMS_HEADER_CSV + "\n" + (DATA_DIR / "test_victims.txt").read_text())

    args = [
        str(collisions_path),
        str(parties_path),
        str(victims_path),
        "-o",
        str(db_path),
    ]
    main(args)
    capsys.readouterr()
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert str(db_path) in captured.err
    assert "already exists" in captured.err


def test_missing_input_exits_before_creating_database(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    collisions = tmp_path / "collisions.txt"
    parties = tmp_path / "parties.txt"
    victims = tmp_path / "victims.txt"
    database = tmp_path / "switrs.sqlite3"
    collisions.touch()
    victims.touch()

    with pytest.raises(SystemExit) as error:
        main([str(collisions), str(parties), str(victims), "-o", str(database)])

    assert error.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Input file not found" in captured.err
    assert str(parties) in captured.err
    assert not database.exists()


def test_empty_input_retains_table_and_continues_import(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    collisions = tmp_path / "collisions.txt"
    parties = tmp_path / "parties.txt"
    victims = tmp_path / "victims.txt"
    database = tmp_path / "switrs.sqlite3"
    collisions.touch()
    parties.write_text(PARTIES_HEADER_CSV + "\n" + (DATA_DIR / "test_parties.txt").read_text())
    victims.write_text(VICTIMS_HEADER_CSV + "\n" + (DATA_DIR / "test_victims.txt").read_text())

    main([str(collisions), str(parties), str(victims), "-o", str(database)])

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"Warning: '{collisions}' is empty, skipping." in captured.err
    with closing(sqlite3.connect(database)) as connection:
        assert connection.execute("SELECT COUNT(*) FROM collisions").fetchone() == (0,)
        assert connection.execute("SELECT COUNT(*) FROM parties").fetchone()[0] > 0
        assert connection.execute("SELECT COUNT(*) FROM victims").fetchone()[0] > 0


@pytest.mark.parametrize("parse_error", ["strict", "ignore"])
def test_cli_uses_default_output_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, parse_error: str
) -> None:
    monkeypatch.chdir(tmp_path)
    input_names = ["collisions.txt", "parties.txt", "victims.txt"]
    for name in input_names:
        (tmp_path / name).touch()

    main([*input_names, "--parse-error", parse_error])

    assert (tmp_path / "switrs.sqlite3").is_file()


def test_cli_rejects_an_unknown_decoding_policy(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["collisions.txt", "parties.txt", "victims.txt", "--parse-error", "unknown"])

    assert error.value.code == 2
    assert "invalid choice: 'unknown'" in capsys.readouterr().err


def test_cli_reports_package_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["--version"])

    assert error.value.code == 0
    assert capsys.readouterr().out.split()[-1] == __version__
