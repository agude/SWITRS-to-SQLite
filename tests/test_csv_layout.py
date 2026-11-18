"""How the physical layout of a CSV file affects the imported rows."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from conftest import COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV

from switrs_to_sqlite.main import convert_files


def import_files(directory: Path, collisions: bytes, parties: bytes) -> Path:
    """Import the given collision and party file contents."""
    collision_path = directory / "collisions.txt"
    party_path = directory / "parties.txt"
    victim_path = directory / "victims.txt"
    database = directory / "switrs.sqlite3"
    collision_path.write_bytes(collisions)
    party_path.write_bytes(parties)
    victim_path.write_text(f"{VICTIMS_HEADER_CSV}\n")
    convert_files(str(collision_path), str(party_path), str(victim_path), str(database))
    return database


def fetch_all(database: Path, query: str) -> list[tuple[object, ...]]:
    with closing(sqlite3.connect(database)) as connection:
        return connection.execute(query).fetchall()


def test_blank_lines_do_not_create_rows(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    database = import_files(
        tmp_path,
        f"{COLLISIONS_HEADER_CSV}\n1\n\n\n2\n\n".encode(),
        f"{PARTIES_HEADER_CSV}\n\n1\n\n".encode(),
    )

    assert fetch_all(database, "SELECT case_id FROM collisions ORDER BY case_id") == [
        ("1",),
        ("2",),
    ]
    assert fetch_all(database, "SELECT case_id FROM parties") == [("1",)]
    errors = capsys.readouterr().err
    assert "collisions: 2 rows total" in errors
    assert "duplicate" not in errors
