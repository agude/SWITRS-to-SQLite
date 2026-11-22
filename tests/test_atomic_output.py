"""The output database appears complete or not at all."""

import os
import stat
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest
from conftest import COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV

import switrs_to_sqlite.main as main_module
from switrs_to_sqlite.main import RecordFileError, convert_files, main

WINNING_DATABASE = b"database from the import that finished first"


def write_inputs(directory: Path, collisions: str = f"{COLLISIONS_HEADER_CSV}\n") -> list[str]:
    contents = (collisions, f"{PARTIES_HEADER_CSV}\n", "")
    paths = [directory / name for name in ("collisions.txt", "parties.txt", "victims.txt")]
    for path, content in zip(paths, contents, strict=True):
        path.write_text(content)
    return [str(path) for path in paths]


def run_before_build(
    monkeypatch: pytest.MonkeyPatch, action: Callable[[Path], object]
) -> list[Path]:
    """Call action with each build path just before the database is written."""
    real_write_database = main_module._write_database
    build_paths: list[Path] = []

    def write_database(output_file: str, *arguments: Any) -> None:
        build_paths.append(Path(output_file))
        action(Path(output_file))
        real_write_database(output_file, *arguments)

    monkeypatch.setattr(main_module, "_write_database", write_database)
    return build_paths


@pytest.fixture
def default_umask() -> Iterator[None]:
    previous_umask = os.umask(0o022)
    yield
    os.umask(previous_umask)


def test_database_is_built_beside_the_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    inputs = write_inputs(tmp_path)
    database = tmp_path / "switrs.sqlite3"

    def assert_destination_absent(_: Path) -> None:
        assert not database.exists()

    build_paths = run_before_build(monkeypatch, assert_destination_absent)

    convert_files(inputs[0], inputs[1], inputs[2], str(database))

    assert build_paths[0].parent.parent == tmp_path
    assert database.is_file()
    assert not build_paths[0].parent.exists()


def test_import_that_loses_the_race_keeps_the_winner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    inputs = write_inputs(tmp_path)
    database = tmp_path / "switrs.sqlite3"
    run_before_build(monkeypatch, lambda _: database.write_bytes(WINNING_DATABASE))

    with pytest.raises(FileExistsError, match="already exists"):
        convert_files(inputs[0], inputs[1], inputs[2], str(database))

    assert database.read_bytes() == WINNING_DATABASE
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "collisions.txt",
        "parties.txt",
        "switrs.sqlite3",
        "victims.txt",
    ]


def test_failed_import_keeps_a_database_created_meanwhile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    inputs = write_inputs(tmp_path, "NOT_A_COLUMN\n")
    database = tmp_path / "switrs.sqlite3"
    run_before_build(monkeypatch, lambda _: database.write_bytes(WINNING_DATABASE))

    with pytest.raises(RecordFileError):
        convert_files(inputs[0], inputs[1], inputs[2], str(database))

    assert database.read_bytes() == WINNING_DATABASE


def test_cli_reports_a_lost_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    inputs = write_inputs(tmp_path)
    database = tmp_path / "switrs.sqlite3"
    run_before_build(monkeypatch, lambda _: database.write_bytes(WINNING_DATABASE))

    with pytest.raises(SystemExit) as error:
        main([*inputs, "-o", str(database)])

    assert error.value.code == 1
    assert f"Error: Output file '{database}' already exists" in capsys.readouterr().err


@pytest.mark.usefixtures("default_umask")
def test_published_database_uses_normal_file_permissions(tmp_path: Path) -> None:
    inputs = write_inputs(tmp_path)
    database = tmp_path / "switrs.sqlite3"

    convert_files(inputs[0], inputs[1], inputs[2], str(database))

    assert stat.S_IMODE(database.stat().st_mode) == 0o644
