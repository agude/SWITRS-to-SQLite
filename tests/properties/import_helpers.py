"""Shared helpers for properties that import generated CSV files."""

import csv
import gzip
import io
from pathlib import Path


def write_csv(
    path: Path,
    headers: list[str],
    records: list[dict[str, str]],
    *,
    compressed: bool,
    has_blank_lines: bool = False,
) -> None:
    """Write CSV records with the standard CSV writer, optionally through gzip."""
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    body = text.getvalue()
    if has_blank_lines:
        body = body.replace("\n", "\n\n")
    payload = "﻿" + body

    if compressed:
        with gzip.open(path, "wt", encoding="utf-8", newline="") as output:
            output.write(payload)
    else:
        path.write_text(payload, encoding="utf-8")
