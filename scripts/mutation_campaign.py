#!/usr/bin/env python3
"""Run mutation testing against scratch copies of the source and tests.

The campaign has two stages:

1. mutmut mutates executable code, apart from CLI help text.
2. This script mutates the column declarations in row_types.py, which mutmut
   cannot reach because they are module-level data.

Any mutmut survivor, or surviving schema mutant that changes parsed values,
fails the campaign.

This module doubles as a pytest plugin. Each schema mutant runs the test suite
with ``-p mutation_campaign`` and SCHEMA_MUTANT set, so the mutation is applied
before any test module imports the parsers.
"""

import dataclasses
import os
import shutil
import subprocess
import sys
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from hypothesis import Phase, settings

import switrs_to_sqlite.parsers as parsers
import switrs_to_sqlite.row_types as row_types
from switrs_to_sqlite.converters import identity
from switrs_to_sqlite.datatypes import DATATYPE_MAP, DataType
from switrs_to_sqlite.schema import Column

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SCRATCH_ROOT = REPOSITORY_ROOT / ".mutation"
TABLE_NAMES = ("COLLISION_ROW", "PARTY_ROW", "VICTIM_ROW")
MUTANT_ENVIRONMENT_VARIABLE = "SCHEMA_MUTANT"
MUTANT_TIMEOUT_SECONDS = 120
PROBE_VALUES = ("", "-", " ", " - ", "x", " x ", "1", " 1 ", "Y", "N", "20200101", "0900")

MUTMUT_CONFIG = """\
[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mutmut]
source_paths = ["src/switrs_to_sqlite"]
only_mutate = [
    "src/switrs_to_sqlite/converters.py",
    "src/switrs_to_sqlite/main.py",
    "src/switrs_to_sqlite/open_record.py",
    "src/switrs_to_sqlite/parsers.py",
    "src/switrs_to_sqlite/schema.py",
]
pytest_add_cli_args_test_selection = ["tests"]
do_not_mutate_patterns = [
    '^\\s+help=',
    '^\\s+description=',
    '^\\s+type=str,',
    '^\\s+"(how to handle|.strict. raises|.ignore. skips|.replace. substitutes)',
]
"""


@dataclass(frozen=True)
class SchemaMutant:
    """One change to one column declaration."""

    table_name: str
    column_index: int
    kind: str

    @property
    def identifier(self) -> str:
        return f"{self.table_name}:{self.column_index}:{self.kind}"

    @classmethod
    def from_identifier(cls, identifier: str) -> "SchemaMutant":
        table_name, column_index, kind = identifier.split(":")
        return cls(table_name, int(column_index), kind)


def table_columns(table_name: str) -> Sequence[Column]:
    columns: Sequence[Column] = getattr(row_types, table_name)
    return columns


def mutated_column(mutant: SchemaMutant) -> Column:
    """Return the changed declaration for a mutant."""
    columns = table_columns(mutant.table_name)
    column = columns[mutant.column_index]
    if mutant.kind == "header":
        other_headers = (other.header for other in columns if other.header != column.header)
        return dataclasses.replace(column, header=next(other_headers))
    if mutant.kind == "type":
        is_text = column.sql_type == DataType.TEXT
        new_type = DataType.INTEGER if is_text else DataType.TEXT
        return dataclasses.replace(column, sql_type=new_type)
    if mutant.kind == "nulls":
        return dataclasses.replace(column, nulls=None if column.nulls else {"", "-"})
    if mutant.kind == "converter":
        return dataclasses.replace(column, converter=identity)
    if mutant.kind == "mapping":
        return dataclasses.replace(column, mapping=None)
    raise ValueError(f"Unknown mutation kind: {mutant.kind}")


def apply_requested_mutant() -> None:
    """Install the mutant named by the environment, when running as a plugin."""
    identifier = os.environ.get(MUTANT_ENVIRONMENT_VARIABLE)
    if identifier is None:
        return

    # Skipping shrinking keeps failing mutants fast.
    settings.register_profile(
        "mutation",
        max_examples=100,
        derandomize=True,
        deadline=None,
        phases=(Phase.explicit, Phase.generate),
    )
    mutant = SchemaMutant.from_identifier(identifier)
    columns = list(table_columns(mutant.table_name))
    columns[mutant.column_index] = mutated_column(mutant)
    # The package __init__ imports parsers first, so both modules hold the table.
    setattr(row_types, mutant.table_name, tuple(columns))
    setattr(parsers, mutant.table_name, tuple(columns))


def parsed_value(column: Column, raw_value: str) -> object:
    converted = column.converter(raw_value, DATATYPE_MAP[column.sql_type], column.nulls)
    return column.mapping.get(converted, converted) if column.mapping else converted


def changes_parsed_values(mutant: SchemaMutant) -> bool:
    """Report whether a null or converter mutant can change a stored value."""
    original = table_columns(mutant.table_name)[mutant.column_index]
    changed = mutated_column(mutant)
    probes = [*PROBE_VALUES, *(original.mapping or ()), *(original.nulls or ())]
    return any(
        repr(parsed_value(original, probe)) != repr(parsed_value(changed, probe))
        for probe in probes
    )


def all_schema_mutants() -> list[SchemaMutant]:
    mutants: list[SchemaMutant] = []
    for table_name in TABLE_NAMES:
        for index, column in enumerate(table_columns(table_name)):
            kinds = ["header", "type", "nulls"]
            if column.converter is not identity:
                kinds.append("converter")
            if column.mapping is not None:
                kinds.append("mapping")
            mutants.extend(SchemaMutant(table_name, index, kind) for kind in kinds)
    return mutants


def copy_project(destination: Path) -> None:
    destination.mkdir(parents=True)
    ignored_names = shutil.ignore_patterns("__pycache__", ".hypothesis")
    for directory in ("src", "tests"):
        shutil.copytree(REPOSITORY_ROOT / directory, destination / directory, ignore=ignored_names)


def campaign_environment(**extra_variables: str) -> dict[str, str]:
    return {
        **os.environ,
        "HYPOTHESIS_PROFILE": "ci",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": f"src{os.pathsep}{REPOSITORY_ROOT / 'scripts'}",
        **extra_variables,
    }


def run_mutmut(scratch_directory: Path) -> int:
    """Run mutmut, print its surviving mutants, and return their number."""
    copy_project(scratch_directory)
    (scratch_directory / "pyproject.toml").write_text(MUTMUT_CONFIG)
    log_path = scratch_directory / "run.log"
    with log_path.open("w") as log:
        subprocess.run(
            ["mutmut", "run"],
            cwd=scratch_directory,
            env=campaign_environment(),
            stdout=log,
            stderr=subprocess.STDOUT,
            check=True,
        )
    results = subprocess.run(
        ["mutmut", "results"],
        cwd=scratch_directory,
        env=campaign_environment(),
        capture_output=True,
        text=True,
        check=True,
    )
    survivors = [line.strip() for line in results.stdout.splitlines() if "survived" in line]
    print(f"mutmut: {len(survivors)} survivors (inspect with mutmut show in {scratch_directory})")
    for survivor in survivors:
        print(f"  {survivor}")
    return len(survivors)


def schema_test_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-x",
        "--no-cov",
        "-p",
        "mutation_campaign",
        "-p",
        "no:cacheprovider",
        "tests",
    ]


def mutant_survives(mutant: SchemaMutant, scratch_directory: Path) -> bool:
    environment = campaign_environment(
        HYPOTHESIS_PROFILE="mutation",
        **{MUTANT_ENVIRONMENT_VARIABLE: mutant.identifier},
    )
    try:
        completed = subprocess.run(
            schema_test_command(),
            cwd=scratch_directory,
            env=environment,
            capture_output=True,
            timeout=MUTANT_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False
    return completed.returncode == 0


def run_schema_mutants(scratch_directory: Path) -> int:
    """Test every schema mutant and return the number of real survivors."""
    copy_project(scratch_directory)
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-x", "--no-cov", "tests"],
        cwd=scratch_directory,
        env=campaign_environment(),
        capture_output=True,
        check=True,
    )

    mutants = all_schema_mutants()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        survived_flags = list(
            executor.map(lambda mutant: mutant_survives(mutant, scratch_directory), mutants)
        )
    survivors = [
        mutant for mutant, survived in zip(mutants, survived_flags, strict=True) if survived
    ]
    real_survivors = [mutant for mutant in survivors if is_real_survivor(mutant)]

    print(
        f"schema: {len(mutants)} mutants, {len(mutants) - len(survivors)} killed, "
        f"{len(survivors) - len(real_survivors)} equivalent, {len(real_survivors)} real survivors"
    )
    for mutant in real_survivors:
        column = table_columns(mutant.table_name)[mutant.column_index]
        print(f"  {mutant.table_name} {column.name}: {mutant.kind}")
    return len(real_survivors)


def is_real_survivor(mutant: SchemaMutant) -> bool:
    """Treat every surviving structural mutant as real; probe value mutants."""
    return mutant.kind not in {"nulls", "converter"} or changes_parsed_values(mutant)


def main() -> int:
    shutil.rmtree(SCRATCH_ROOT, ignore_errors=True)
    mutmut_survivors = run_mutmut(SCRATCH_ROOT / "mutmut")
    schema_survivors = run_schema_mutants(SCRATCH_ROOT / "schema")
    return 1 if mutmut_survivors or schema_survivors else 0


if __name__ == "__main__":
    sys.exit(main())
else:
    apply_requested_mutant()
