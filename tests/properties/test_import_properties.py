"""Model-based properties for importing legacy CSV files into SQLite."""

import contextlib
import csv
import gzip
import io
import sqlite3
import tempfile
from pathlib import Path

from conftest import COLLISION_HEADER, PARTY_HEADER, VICTIM_HEADER
from hypothesis import given, settings
from hypothesis import strategies as st

from switrs_to_sqlite.main import convert_files


def write_csv(
    path: Path, headers: list[str], records: list[dict[str, str]], *, compressed: bool
) -> None:
    """Write CSV records with the standard CSV writer, optionally through gzip."""
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    payload = "\ufeff" + text.getvalue()
    if compressed:
        with gzip.open(path, "wt", encoding="utf-8", newline="") as output:
            output.write(payload)
    else:
        path.write_text(payload, encoding="utf-8")


def records_for_keys(
    headers: list[str], keys: list[str], *, number_field: str | None = None
) -> list[dict[str, str]]:
    """Build simple records with observable keys and row numbers."""
    records = []
    for number, case_id in enumerate(keys, start=1):
        record = dict.fromkeys(headers, "")
        record["CASE_ID"] = case_id
        if number_field is not None:
            record[number_field] = str(number)
        records.append(record)
    return records


def assert_import(
    directory: Path,
    collision_keys: list[str],
    party_keys: list[str],
    victim_keys: list[str],
    *,
    compressed: bool,
    reverse_headers: bool,
) -> None:
    collision_headers = [*COLLISION_HEADER, "UNUSED_COLUMN"]
    party_headers = list(PARTY_HEADER)
    victim_headers = list(VICTIM_HEADER)
    if reverse_headers:
        collision_headers.reverse()
        party_headers.reverse()
        victim_headers.reverse()

    collisions = records_for_keys(collision_headers, collision_keys)
    for occurrence, record in enumerate(collisions):
        record["JURIS"] = str(100 + occurrence)
        record["PRIMARY_RD"] = f'Road, "{occurrence}"'
        record["UNUSED_COLUMN"] = "ignored"
    parties = records_for_keys(party_headers, party_keys, number_field="PARTY_NUMBER")
    victims = records_for_keys(victim_headers, victim_keys, number_field="PARTY_NUMBER")

    # Gzip detection is based on file contents, so both encodings share extensions.
    collision_path = directory / "collisions.csv"
    party_path = directory / "parties.csv"
    victim_path = directory / "victims.csv"
    database_path = directory / "output.sqlite3"
    write_csv(collision_path, collision_headers, collisions, compressed=compressed)
    write_csv(party_path, party_headers, parties, compressed=compressed)
    write_csv(victim_path, victim_headers, victims, compressed=compressed)

    convert_files(str(collision_path), str(party_path), str(victim_path), str(database_path))

    expected_collision_by_key: dict[str, tuple[int, str]] = {}
    for occurrence, case_id in enumerate(collision_keys):
        expected_collision_by_key.setdefault(case_id, (100 + occurrence, f'Road, "{occurrence}"'))

    with contextlib.closing(sqlite3.connect(database_path)) as database:
        actual_collisions = list(
            database.execute(
                "SELECT case_id, jurisdiction, primary_road FROM collisions ORDER BY case_id"
            )
        )
        assert actual_collisions == [
            (case_id, *expected_collision_by_key[case_id])
            for case_id in sorted(expected_collision_by_key)
        ]
        assert list(database.execute("SELECT case_id, party_number FROM parties ORDER BY id")) == [
            (case_id, number) for number, case_id in enumerate(party_keys, start=1)
        ]
        assert list(database.execute("SELECT case_id, party_number FROM victims ORDER BY id")) == [
            (case_id, number) for number, case_id in enumerate(victim_keys, start=1)
        ]


@settings(deadline=None)
@given(
    collision_keys=st.lists(
        st.integers(min_value=1, max_value=8).map(str), min_size=0, max_size=12
    ),
    party_keys=st.lists(st.integers(min_value=1, max_value=8).map(str), min_size=0, max_size=15),
    victim_keys=st.lists(st.integers(min_value=1, max_value=8).map(str), min_size=0, max_size=15),
    compressed=st.booleans(),
    reverse_headers=st.booleans(),
)
def test_import_preserves_first_collision_and_child_multiplicity(
    collision_keys: list[str],
    party_keys: list[str],
    victim_keys: list[str],
    compressed: bool,
    reverse_headers: bool,
) -> None:
    """Imports deduplicate collisions by case ID and retain every child row."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        assert_import(
            Path(temporary_directory),
            collision_keys,
            party_keys,
            victim_keys,
            compressed=compressed,
            reverse_headers=reverse_headers,
        )
