"""Regression test for integers outside SQLite's storage range."""

import csv
import sqlite3
from contextlib import closing
from pathlib import Path

from conftest import COLLISION_HEADER, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV

from switrs_to_sqlite.main import convert_files


def test_import_stores_out_of_range_integer_as_null(tmp_path: Path) -> None:
    collisions = tmp_path / "collisions.txt"
    parties = tmp_path / "parties.txt"
    victims = tmp_path / "victims.txt"
    database = tmp_path / "switrs.sqlite3"
    record = dict.fromkeys(COLLISION_HEADER, "")
    record.update(CASE_ID="1", JURIS="99999999999999999999")
    with collisions.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=COLLISION_HEADER)
        writer.writeheader()
        writer.writerow(record)
    parties.write_text(PARTIES_HEADER_CSV + "\n")
    victims.write_text(VICTIMS_HEADER_CSV + "\n")

    convert_files(str(collisions), str(parties), str(victims), str(database))

    with closing(sqlite3.connect(database)) as connection:
        assert connection.execute("SELECT case_id, jurisdiction FROM collisions").fetchall() == [
            ("1", None)
        ]
