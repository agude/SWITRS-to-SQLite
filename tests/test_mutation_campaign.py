"""The mutation campaign must not pass on inconclusive results."""

import subprocess
from pathlib import Path
from typing import Any

import mutation_campaign as campaign
import pytest
from mutation_campaign import MutantOutcome, SchemaMutant

MUTANT = SchemaMutant("COLLISION_ROW", 0, "header")
OTHER_MUTANT = SchemaMutant("PARTY_ROW", 0, "header")


def completed(returncode: int = 0, stdout: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], returncode, stdout=stdout)


@pytest.mark.parametrize(
    ("exit_code", "expected"),
    [
        (0, MutantOutcome.SURVIVED),
        (1, MutantOutcome.KILLED),
        (2, MutantOutcome.UNRESOLVED),
        (3, MutantOutcome.UNRESOLVED),
        (4, MutantOutcome.UNRESOLVED),
        (5, MutantOutcome.UNRESOLVED),
    ],
)
def test_only_test_results_are_conclusive(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, exit_code: int, expected: MutantOutcome
) -> None:
    monkeypatch.setattr(subprocess, "run", lambda *_, **__: completed(exit_code))

    assert campaign.mutant_outcome(MUTANT, tmp_path) is expected


def test_timeout_is_unresolved(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def time_out(*_: Any, **__: Any) -> None:
        raise subprocess.TimeoutExpired("pytest", 1)

    monkeypatch.setattr(subprocess, "run", time_out)

    assert campaign.mutant_outcome(MUTANT, tmp_path) is MutantOutcome.UNRESOLVED


def test_schema_stage_counts_unresolved_mutants(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    outcomes = {MUTANT: MutantOutcome.KILLED, OTHER_MUTANT: MutantOutcome.UNRESOLVED}
    monkeypatch.setattr(campaign, "copy_project", lambda _: None)
    monkeypatch.setattr(subprocess, "run", lambda *_, **__: completed())
    monkeypatch.setattr(campaign, "all_schema_mutants", lambda: list(outcomes))
    monkeypatch.setattr(campaign, "mutant_outcome", lambda mutant, _: outcomes[mutant])

    assert campaign.run_schema_mutants(tmp_path) == 1

    output = capsys.readouterr().out
    assert "1 killed" in output
    assert "1 unresolved" in output
    assert "PARTY_ROW case_id: header (unresolved)" in output


def test_mutmut_stage_counts_every_unkilled_status(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    results = (
        "    package.first__mutmut_1: survived\n"
        "    package.second__mutmut_2: timeout\n"
        "    package.third__mutmut_3: suspicious\n"
        "    package.fourth__mutmut_4: no tests\n"
    )

    def run_mutmut_command(command: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        return completed(stdout=results if command[1] == "results" else "")

    monkeypatch.setattr(campaign, "copy_project", lambda directory: directory.mkdir())
    monkeypatch.setattr(subprocess, "run", run_mutmut_command)

    assert campaign.run_mutmut(tmp_path / "scratch") == 4


@pytest.mark.parametrize(
    ("mutmut_failures", "schema_failures", "expected"),
    [(0, 0, 0), (1, 0, 1), (0, 1, 1)],
)
def test_campaign_fails_on_any_unresolved_stage(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    mutmut_failures: int,
    schema_failures: int,
    expected: int,
) -> None:
    monkeypatch.setattr(campaign, "SCRATCH_ROOT", tmp_path / "scratch")
    monkeypatch.setattr(campaign, "run_mutmut", lambda _: mutmut_failures)
    monkeypatch.setattr(campaign, "run_schema_mutants", lambda _: schema_failures)

    assert campaign.main() == expected
