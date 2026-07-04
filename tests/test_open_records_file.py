#!/usr/bin/env python3

import gzip
from pathlib import Path
from typing import Any

from switrs_to_sqlite.open_record import open_record_file


def test_read_gzipped_file(tmpdir: Any) -> None:
    # Write a file to read back
    contents = "Test contents\nsecond line"
    file_path = Path(tmpdir) / "test.csv.gz"
    with gzip.open(file_path, "wt") as f:
        f.write(contents)

    # Read back the file
    with open_record_file(str(file_path)) as f:
        assert f.read() == contents


def test_read_normal_file(tmpdir: Any) -> None:
    # Write a file to read back
    contents = "Test contents\nsecond line"
    file_path = Path(tmpdir) / "test.csv"
    file_path.write_text(contents)

    # Read back the file
    with open_record_file(str(file_path)) as f:
        assert f.read() == contents
