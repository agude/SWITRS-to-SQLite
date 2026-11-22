"""The fixture extractor must preserve field contents."""

import csv
import io
from pathlib import Path

from extract_test_rows import analyze_file, extract_rows


def test_extracted_rows_round_trip_special_characters(tmp_path: Path) -> None:
    records = [
        ['say "hi"', "comma, inside", "plain"],
        ["line\nbreak", "carriage\r\nreturn", "cr\ronly"],
    ]
    source = tmp_path / "records.txt"
    with source.open("w", newline="", encoding="utf-8") as output:
        # Python 3.10 quotes a lone CR only when it is part of the line terminator.
        writer = csv.writer(output, lineterminator="\r\n")
        writer.writerow(["FIRST", "SECOND", "THIRD"])
        writer.writerows(records)

    data = analyze_file(str(source), {}, {})
    extracted = extract_rows(data, [0, 1])

    assert data["rows"] == records
    parsed = [next(csv.reader(io.StringIO(row, newline=""))) for row in extracted]
    assert parsed == records
