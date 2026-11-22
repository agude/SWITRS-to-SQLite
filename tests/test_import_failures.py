"""Failed imports report one error and leave no partial database."""

import gzip
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV

from switrs_to_sqlite.main import main

HEADERS = (COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV)
CSV_FIELD_LIMIT = 131_072


def compressed_rows(header: str) -> bytes:
    """Compress enough rows that the stream has a body to damage."""
    rows = "".join(f"{number}\n" for number in range(1_000))
    return gzip.compress(f"{header}\n{rows}".encode())


def missing_header(header: str) -> bytes:
    return b"NOT_A_COLUMN\n1\n"


def invalid_utf8(header: str) -> bytes:
    return f"{header}\n".encode() + b"\xff\n"


def truncated_gzip(header: str) -> bytes:
    payload = compressed_rows(header)
    return payload[: len(payload) // 2]


def corrupted_gzip(header: str) -> bytes:
    payload = bytearray(compressed_rows(header))
    payload[len(payload) // 2] ^= 0xFF
    return bytes(payload)


def oversized_field(header: str) -> bytes:
    return f"{header}\n{'x' * (CSV_FIELD_LIMIT + 1)}\n".encode()


def unterminated_quote(header: str) -> bytes:
    return f'{header}\n"1\n2\n'.encode()


def quote_spanning_records(header: str) -> bytes:
    return f'{header}\n"1\n2" street\n3\n'.encode()


def write_inputs(
    directory: Path, bad_index: int | None, make_bad: Callable[[str], bytes]
) -> list[str]:
    """Write three header-only inputs, damaging the one at bad_index."""
    paths = []
    for index, header in enumerate(HEADERS):
        path = directory / f"input_{index}.txt"
        payload = make_bad(header) if index == bad_index else f"{header}\n".encode()
        path.write_bytes(payload)
        paths.append(str(path))
    return paths


@pytest.mark.parametrize("bad_index", [0, 1, 2])
@pytest.mark.parametrize(
    "make_bad",
    [
        missing_header,
        invalid_utf8,
        truncated_gzip,
        corrupted_gzip,
        oversized_field,
        unterminated_quote,
        quote_spanning_records,
    ],
)
def test_bad_input_exits_cleanly_and_allows_a_rerun(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    bad_index: int,
    make_bad: Callable[[str], bytes],
) -> None:
    inputs = write_inputs(tmp_path, bad_index, make_bad)
    database = tmp_path / "switrs.sqlite3"

    with pytest.raises(SystemExit) as error:
        main([*inputs, "-o", str(database)])

    assert error.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.splitlines()[-1].startswith(
        f"Error: Could not convert '{inputs[bad_index]}'"
    )
    assert not database.exists()

    repaired_inputs = write_inputs(tmp_path, None, make_bad)
    main([*repaired_inputs, "-o", str(database)])
    assert database.is_file()


def test_directory_input_exits_cleanly(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    inputs = write_inputs(tmp_path, None, missing_header)
    directory_input = tmp_path / "directory"
    directory_input.mkdir()
    inputs[1] = str(directory_input)
    database = tmp_path / "switrs.sqlite3"

    with pytest.raises(SystemExit) as error:
        main([*inputs, "-o", str(database)])

    assert error.value.code == 1
    assert f"Could not convert '{directory_input}'" in capsys.readouterr().err
    assert not database.exists()


def test_unwritable_output_exits_cleanly(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    inputs = write_inputs(tmp_path, None, missing_header)
    database = tmp_path / "missing_directory" / "switrs.sqlite3"

    with pytest.raises(SystemExit) as error:
        main([*inputs, "-o", str(database)])

    assert error.value.code == 1
    assert f"Could not write '{database}'" in capsys.readouterr().err
