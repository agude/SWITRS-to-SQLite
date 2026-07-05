#!/usr/bin/env python3
"""Generate golden snapshot data for integration tests.

This script creates a golden_snapshot.json file containing expected database
output for the test data files. Run this whenever the parser logic changes
to update the expected values.

Usage:
    python scripts/generate_golden.py
"""

import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tests"))

from conftest import (  # noqa: E402
    COLLISIONS_HEADER_CSV,
    PARTIES_HEADER_CSV,
    VICTIMS_HEADER_CSV,
)

from switrs_to_sqlite.main import main  # noqa: E402

# Paths relative to project root
TESTS_DATA_DIR = PROJECT_ROOT / "tests" / "data"
GOLDEN_SNAPSHOT_PATH = TESTS_DATA_DIR / "golden_snapshot.json"


def create_input_files(temp_dir: Path) -> tuple[Path, Path, Path]:
    """Create temporary input files with headers prepended."""
    # Read raw data files
    collisions_data = (TESTS_DATA_DIR / "test_collisions.txt").read_text()
    parties_data = (TESTS_DATA_DIR / "test_parties.txt").read_text()
    victims_data = (TESTS_DATA_DIR / "test_victims.txt").read_text()

    # Write files with headers
    collisions_path = temp_dir / "collisions.txt"
    parties_path = temp_dir / "parties.txt"
    victims_path = temp_dir / "victims.txt"

    collisions_path.write_text(COLLISIONS_HEADER_CSV + "\n" + collisions_data)
    parties_path.write_text(PARTIES_HEADER_CSV + "\n" + parties_data)
    victims_path.write_text(VICTIMS_HEADER_CSV + "\n" + victims_data)

    return collisions_path, parties_path, victims_path


def generate_golden_data() -> None:
    """Generate golden snapshot data and write to JSON file."""
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create input files
        collisions_path, parties_path, victims_path = create_input_files(temp_path)
        db_path = temp_path / "golden.sqlite3"

        # Run the converter using dependency injection
        main(
            [
                str(collisions_path),
                str(parties_path),
                str(victims_path),
                "-o",
                str(db_path),
            ]
        )

        # Extract data from database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        tables = ["collisions", "parties", "victims"]
        golden_data: dict[str, Any] = {}

        for table in tables:
            # Get columns to ensure order
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in cursor.fetchall()]

            # Get rows ordered by appropriate key
            sort_col = "id" if "id" in columns else "case_id"
            cursor.execute(f"SELECT * FROM {table} ORDER BY {sort_col}")
            rows = [list(row) for row in cursor.fetchall()]

            golden_data[table] = {"columns": columns, "rows": rows}

        # Write JSON output
        GOLDEN_SNAPSHOT_PATH.write_text(
            json.dumps(golden_data, indent=2, ensure_ascii=False) + "\n"
        )
        print(f"Golden snapshot written to: {GOLDEN_SNAPSHOT_PATH}")

        # Run custom logic checks for verification
        check_custom_logic(cursor)

        conn.close()


def check_custom_logic(cursor: sqlite3.Cursor) -> None:
    """Run verification checks for specific test cases."""
    print("\n--- Custom Logic Checks ---")

    # 81335356: Chevrolet mapping (CHEVY -> chevrolet)
    cursor.execute("SELECT vehicle_make FROM parties WHERE case_id='81335356'")
    print(f"81335356 Make: {cursor.fetchall()}")

    # 3899454: Pedestrian Collision
    cursor.execute(
        "SELECT pedestrian_collision FROM collisions WHERE case_id='3899454'"
    )
    print(f"3899454 Ped Flag: {cursor.fetchone()}")
    cursor.execute("SELECT party_type FROM parties WHERE case_id='3899454'")
    print(f"3899454 Party Types: {cursor.fetchall()}")

    # 0726202: Hit and Run
    cursor.execute("SELECT hit_and_run FROM collisions WHERE case_id='0726202'")
    print(f"0726202 Hit&Run: {cursor.fetchone()}")

    # 3982906: Motorcycle
    cursor.execute(
        "SELECT motorcycle_collision FROM collisions WHERE case_id='3982906'"
    )
    print(f"3982906 MC Flag: {cursor.fetchone()}")
    cursor.execute(
        "SELECT vehicle_make FROM parties WHERE case_id='3982906' AND party_number=2"
    )
    print(f"3982906 MC Make: {cursor.fetchone()}")


if __name__ == "__main__":
    generate_golden_data()
