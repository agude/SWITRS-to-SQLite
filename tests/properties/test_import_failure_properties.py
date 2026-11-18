"""Any damaged input file fails cleanly and leaves no database behind."""

import contextlib
import gzip
import io
import tempfile
from pathlib import Path

import pytest
from conftest import COLLISION_HEADER, PARTY_HEADER, VICTIM_HEADER
from hypothesis import given, settings
from hypothesis import strategies as st

from switrs_to_sqlite.main import main
from switrs_to_sqlite.row_types import COLLISION_ROW, PARTY_ROW, VICTIM_ROW

HEADERS = (COLLISION_HEADER, PARTY_HEADER, VICTIM_HEADER)
TABLE_ROWS = (COLLISION_ROW, PARTY_ROW, VICTIM_ROW)
INPUT_INDICES = st.integers(min_value=0, max_value=len(HEADERS) - 1)


def valid_payload(headers: list[str]) -> bytes:
    rows = "".join(f"{number}\n" for number in range(200))
    return f"{','.join(headers)}\n{rows}".encode()


def assert_clean_failure(bad_index: int, bad_payload: bytes) -> None:
    """Import with one damaged file and check the CLI failure contract."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory)
        inputs = [directory / f"input_{index}.txt" for index in range(len(HEADERS))]
        for index, (path, headers) in enumerate(zip(inputs, HEADERS, strict=True)):
            path.write_bytes(bad_payload if index == bad_index else valid_payload(headers))
        database = directory / "output.sqlite3"
        errors = io.StringIO()

        with contextlib.redirect_stderr(errors), pytest.raises(SystemExit) as failure:
            main([*map(str, inputs), "-o", str(database)])

        assert failure.value.code == 1
        expected_prefix = f"Error: Could not convert '{inputs[bad_index]}'"
        assert errors.getvalue().splitlines()[-1].startswith(expected_prefix)
        assert not database.exists()


@settings(deadline=None)
@given(bad_index=INPUT_INDICES, cut=st.integers(min_value=2, max_value=2_000))
def test_truncated_gzip_fails_cleanly(bad_index: int, cut: int) -> None:
    payload = gzip.compress(valid_payload(HEADERS[bad_index]))
    assert_clean_failure(bad_index, payload[: min(cut, len(payload) - 1)])


@settings(deadline=None)
@given(bad_index=INPUT_INDICES, row_number=st.integers(min_value=1, max_value=200))
def test_invalid_utf8_fails_cleanly(bad_index: int, row_number: int) -> None:
    lines = valid_payload(HEADERS[bad_index]).splitlines(keepends=True)
    lines[row_number] = b"\xff" + lines[row_number]
    assert_clean_failure(bad_index, b"".join(lines))


@settings(deadline=None)
@given(data=st.data(), bad_index=INPUT_INDICES)
def test_missing_required_header_fails_cleanly(data: st.DataObject, bad_index: int) -> None:
    headers = HEADERS[bad_index]
    required_headers = sorted({column.header.upper() for column in TABLE_ROWS[bad_index]})
    missing = data.draw(st.sampled_from(required_headers))
    remaining = [header for header in headers if header != missing]
    assert_clean_failure(bad_index, f"{','.join(remaining)}\n1\n".encode())
