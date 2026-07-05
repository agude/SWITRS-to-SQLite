"""Integration tests for SWITRS to SQLite conversion.

Tests end-to-end conversion of raw SWITRS CSV data to SQLite database,
comparing output against a golden snapshot file.
"""

import gzip
import json
import sqlite3
from pathlib import Path
from typing import Any

from conftest import COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV

from switrs_to_sqlite.main import main

# Paths
DATA_DIR = Path(__file__).parent / "data"
GOLDEN_SNAPSHOT = DATA_DIR / "golden_snapshot.json"


def load_golden_data() -> dict[str, Any]:
    """Load expected data from golden snapshot JSON file."""
    with GOLDEN_SNAPSHOT.open() as f:
        result: dict[str, Any] = json.load(f)
        return result


def test_end_to_end(tmp_path: Path) -> None:
    """Test complete conversion pipeline against golden snapshot."""
    # Set up paths
    collisions_path = tmp_path / "collisions.txt"
    parties_path = tmp_path / "parties.txt"
    victims_path = tmp_path / "victims.txt"
    db_path = tmp_path / "switrs.sqlite3"

    # Read raw data from tests/data/
    collisions_data = (DATA_DIR / "test_collisions.txt").read_text()
    parties_data = (DATA_DIR / "test_parties.txt").read_text()
    victims_data = (DATA_DIR / "test_victims.txt").read_text()

    # Write input CSVs with headers
    collisions_path.write_text(COLLISIONS_HEADER_CSV + "\n" + collisions_data)
    parties_path.write_text(PARTIES_HEADER_CSV + "\n" + parties_data)
    victims_path.write_text(VICTIMS_HEADER_CSV + "\n" + victims_data)

    # Run conversion using dependency injection
    main(
        [
            str(collisions_path),
            str(parties_path),
            str(victims_path),
            "-o",
            str(db_path),
        ]
    )

    # Verify database was created
    assert db_path.exists(), "Database file was not created"

    # Load golden data
    expected_data = load_golden_data()

    # Connect and verify
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for table_name, expected_content in expected_data.items():
            expected_columns = expected_content["columns"]
            expected_rows = expected_content["rows"]

            # Check columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            actual_columns = [info[1] for info in cursor.fetchall()]

            assert actual_columns == expected_columns, (
                f"Columns for table '{table_name}' do not match golden data.\n"
                f"Expected: {expected_columns}\n"
                f"Actual:   {actual_columns}"
            )

            # Check rows (ordered by primary key for stability)
            sort_col = "id" if "id" in actual_columns else "case_id"
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY {sort_col}")
            actual_rows = cursor.fetchall()

            # Assert row count matches
            assert len(actual_rows) == len(expected_rows), (
                f"Row count for table '{table_name}' does not match.\n"
                f"Expected: {len(expected_rows)}\n"
                f"Actual:   {len(actual_rows)}"
            )

            # Assert content (convert JSON arrays to tuples for comparison)
            for i, (actual_row, expected_row) in enumerate(
                zip(actual_rows, expected_rows, strict=True)
            ):
                expected_tuple = tuple(expected_row)
                assert actual_row == expected_tuple, (
                    f"Row {i} in table '{table_name}' does not match golden data.\n"
                    f"Expected: {expected_tuple}\n"
                    f"Actual:   {actual_row}"
                )
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
        )
        indices = {row[0] for row in cursor.fetchall()}
        assert indices == {"idx_parties_case_id", "idx_victims_case_id"}
    finally:
        conn.close()


def test_end_to_end_gzipped(tmp_path: Path) -> None:
    """Gzipped input files produce identical output to plain text."""
    collisions_path = tmp_path / "collisions.txt.gz"
    parties_path = tmp_path / "parties.txt.gz"
    victims_path = tmp_path / "victims.txt.gz"
    db_path = tmp_path / "switrs.sqlite3"

    collisions_data = (DATA_DIR / "test_collisions.txt").read_text()
    parties_data = (DATA_DIR / "test_parties.txt").read_text()
    victims_data = (DATA_DIR / "test_victims.txt").read_text()

    for path, header, data in (
        (collisions_path, COLLISIONS_HEADER_CSV, collisions_data),
        (parties_path, PARTIES_HEADER_CSV, parties_data),
        (victims_path, VICTIMS_HEADER_CSV, victims_data),
    ):
        with gzip.open(path, "wt", encoding="utf-8-sig") as f:
            f.write(header + "\n" + data)

    main(
        [
            str(collisions_path),
            str(parties_path),
            str(victims_path),
            "-o",
            str(db_path),
        ]
    )

    expected_data = load_golden_data()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for table_name, expected_content in expected_data.items():
            sort_col = "id" if "id" in expected_content["columns"] else "case_id"
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY {sort_col}")
            actual_rows = cursor.fetchall()
            for i, (actual_row, expected_row) in enumerate(
                zip(actual_rows, expected_content["rows"], strict=True)
            ):
                assert actual_row == tuple(expected_row), (
                    f"Row {i} in table '{table_name}' differs for gzipped input"
                )
    finally:
        conn.close()


def test_parse_error_replace(tmp_path: Path) -> None:
    """The --parse-error replace flag substitutes invalid bytes."""
    collisions_path = tmp_path / "collisions.txt"
    parties_path = tmp_path / "parties.txt"
    victims_path = tmp_path / "victims.txt"
    db_path = tmp_path / "switrs.sqlite3"

    # Write valid parties and victims
    parties_data = (DATA_DIR / "test_parties.txt").read_text()
    victims_data = (DATA_DIR / "test_victims.txt").read_text()
    parties_path.write_text(PARTIES_HEADER_CSV + "\n" + parties_data)
    victims_path.write_text(VICTIMS_HEADER_CSV + "\n" + victims_data)

    # Write collisions with an invalid byte in the first data row
    header_bytes = (COLLISIONS_HEADER_CSV + "\n").encode("utf-8")
    data_bytes = (DATA_DIR / "test_collisions.txt").read_text().encode("utf-8")
    # Corrupt a byte in the data portion (not the header)
    data_bytes = data_bytes[:10] + b"\xff\xfe" + data_bytes[10:]
    collisions_path.write_bytes(header_bytes + data_bytes)

    main(
        [
            str(collisions_path),
            str(parties_path),
            str(victims_path),
            "-o",
            str(db_path),
            "-p",
            "replace",
        ]
    )

    assert db_path.exists()
