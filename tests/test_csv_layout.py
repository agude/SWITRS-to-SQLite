"""How the physical layout of a CSV file affects the imported rows."""

import csv
import gzip
import io
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from conftest import COLLISION_HEADER, COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV

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


def collision_file_with_road(road: str) -> bytes:
    record = dict.fromkeys(COLLISION_HEADER, "")
    record.update(CASE_ID="1", PRIMARY_RD=road)
    text = io.StringIO(newline="")
    # Python 3.10 quotes a lone CR only when it is part of the line terminator.
    writer = csv.DictWriter(text, fieldnames=COLLISION_HEADER, lineterminator="\r\n")
    writer.writeheader()
    writer.writerow(record)
    return text.getvalue().encode()


@pytest.mark.parametrize("compressed", [False, True])
@pytest.mark.parametrize("road", ["Main\r\nStreet", "Main\rStreet", "Main\nStreet"])
def test_quoted_line_breaks_are_preserved(tmp_path: Path, compressed: bool, road: str) -> None:
    collisions = collision_file_with_road(road)
    if compressed:
        collisions = gzip.compress(collisions)

    database = import_files(tmp_path, collisions, f"{PARTIES_HEADER_CSV}\n".encode())

    assert fetch_all(database, "SELECT primary_road FROM collisions") == [(road,)]


@pytest.mark.parametrize("line_ending", ["\n", "\r\n", "\r"])
def test_record_line_endings_are_equivalent(tmp_path: Path, line_ending: str) -> None:
    collisions = line_ending.join([COLLISIONS_HEADER_CSV, "1", "2", ""]).encode()

    database = import_files(tmp_path, collisions, f"{PARTIES_HEADER_CSV}\n".encode())

    assert fetch_all(database, "SELECT case_id FROM collisions ORDER BY case_id") == [
        ("1",),
        ("2",),
    ]


def collision_line(**raw_fields: str) -> str:
    """Join raw, already-quoted field text into one collision record line."""
    fields = dict.fromkeys(COLLISION_HEADER, "")
    fields.update(raw_fields)
    return ",".join(fields[header] for header in COLLISION_HEADER)


# Raw field text from the 20160924 and 20210604 CHP exports, paired with the
# values v5.1.0 stored for it.
UNESCAPED_QUOTE_ROADS = [
    ('"O"NEILL ST"', 'ONEILL ST"'),
    ('"RYAN"S GATE"', 'RYANS GATE"'),
    ('""A" ST."', 'A" ST."'),
    ('"I-5 N/B TO "Q ST E/B"', 'I-5 N/B TO Q ST E/B"'),
]


@pytest.mark.parametrize(("raw_road", "stored_road"), UNESCAPED_QUOTE_ROADS)
def test_unescaped_quotes_parse_as_in_v5_1_0(
    tmp_path: Path, raw_road: str, stored_road: str
) -> None:
    line = collision_line(CASE_ID="1", PRIMARY_RD=raw_road, SECONDARY_RD='"ELM ST"')
    collisions = f"{COLLISIONS_HEADER_CSV}\n{line}\n".encode()

    database = import_files(tmp_path, collisions, f"{PARTIES_HEADER_CSV}\n".encode())

    assert fetch_all(database, "SELECT primary_road, secondary_road FROM collisions") == [
        (stored_road, "ELM ST")
    ]


def test_escaped_quote_before_delimiter_joins_fields_as_in_v5_1_0(tmp_path: Path) -> None:
    # CHP wrote 73' 0" as "73' 0"", which escapes the quote and leaves the field
    # open through the next field's opening quote.
    line = collision_line(CASE_ID="1", SECONDARY_RD='"73\' 0""', DISTANCE='"0.00"')
    collisions = f"{COLLISIONS_HEADER_CSV}\n{line}\n".encode()

    database = import_files(tmp_path, collisions, f"{PARTIES_HEADER_CSV}\n".encode())

    assert fetch_all(database, "SELECT secondary_road FROM collisions") == [('73\' 0",0.00"',)]
