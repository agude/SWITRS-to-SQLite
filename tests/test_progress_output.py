"""Progress reporting during an import."""

import io
import sys
from pathlib import Path

import pytest
from conftest import COLLISIONS_HEADER_CSV, PARTIES_HEADER_CSV, VICTIMS_HEADER_CSV

import switrs_to_sqlite.main as main_module


class FlushRecordingStream(io.StringIO):
    """Record the text written so far each time the stream is flushed."""

    def __init__(self) -> None:
        super().__init__()
        self.flushed_text: list[str] = []

    def flush(self) -> None:
        self.flushed_text.append(self.getvalue())


def test_import_reports_progress_on_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    collisions = tmp_path / "collisions.txt"
    parties = tmp_path / "parties.txt"
    victims = tmp_path / "victims.txt"
    collisions.write_text(f"{COLLISIONS_HEADER_CSV}\n1\n2\n3\n")
    parties.write_text(f"{PARTIES_HEADER_CSV}\n")
    victims.write_text(f"{VICTIMS_HEADER_CSV}\n")
    progress = FlushRecordingStream()
    monkeypatch.setattr(main_module, "_PROGRESS_INTERVAL", 2)
    monkeypatch.setattr(sys, "stderr", progress)

    main_module.convert_files(
        str(collisions), str(parties), str(victims), str(tmp_path / "switrs.sqlite3")
    )

    assert progress.getvalue() == (
        "Converting collisions...\n"
        "  2 rows\n"
        "  collisions: 3 rows total\n"
        "Converting parties...\n"
        "  parties: 0 rows total\n"
        "Converting victims...\n"
        "  victims: 0 rows total\n"
    )
    assert "Converting collisions...\n  2 rows\n" in progress.flushed_text
    assert capsys.readouterr().out == ""
