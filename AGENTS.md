# AGENTS.md

`CLAUDE.md` and `GEMINI.md` are symlinks to this file.

## Context

SWITRS-to-SQLite converts the California Highway Patrol's SWITRS CSV exports
(`CollisionRecords.txt`, `PartyRecords.txt`, `VictimRecords.txt`) into a single
SQLite database. It is published to PyPI and follows SemVer: the MAJOR version
increments when either the command line or the output database structure
changes incompatibly.

CHP retired iSWITRS in January 2025 in favour of CCRS, which uses a different
layout. This tool handles the legacy format only; CCRS lives in a separate
project.

## Operations

All work goes through `just` (see the project-standards skill for the verb
contract). Every check has one definition here; the pre-commit hook and CI
call these same recipes rather than restating commands.

```bash
just sync         # install dependencies
just lint         # ruff check + ruff format --check (read-only)
just format       # ruff format + ruff check --fix (mutating)
just type-check   # mypy, strict
just test         # pytest with the 90% coverage gate
just check        # everything CI runs: lint + type-check + test
just hooks-install  # install bin/pre-commit.sh into this clone
```

## Layout

- `src/switrs_to_sqlite/` — the package. `__init__.py` holds `__version__`,
  which is the single source of the version: hatchling reads it at build time
  and the CLI prints it for `--version`.
- `tests/` — pytest suite; coverage must stay at or above 90%.
- `scripts/` — maintenance helpers (golden-file generation, test-row
  extraction). Type-checked along with the package.
- `bin/pre-commit.sh` — the hook; installed by `just hooks-install`.

## Releasing

1. Bump `__version__` in `src/switrs_to_sqlite/__init__.py`. Nothing else
   stores the version.
2. Commit, tag `vX.Y.Z`, push the tag.
3. Publish a GitHub release. `release.yml` runs the full CI pipeline, verifies
   the tag matches `__version__`, then publishes to PyPI via trusted
   publishing.

A tag that disagrees with `__version__` fails the release job by design.
