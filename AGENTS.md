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

## `make_map.py` conventions

`src/switrs_to_sqlite/make_map.py` maps raw vehicle-make strings to canonical
makes. The traps, in the order they have actually bitten:

- **Model names resolve to their make** — `ODYSSEY` → Honda, `RANGER` → Ford,
  `PRIUS` → Toyota. Field truncations stay with the truncated make:
  `RANGE RO` → Land Rover.
- **NCIC vehicle make codes are authoritative** for abbreviations —
  `INTL` → International Harvester.
- **TaoTao (`TAOTA` / `TAOTAO`) is a real Chinese scooter and ATV maker**, not
  a Toyota typo. It gets its own make.
- **Some mappings are deliberately ambiguous and must be left alone:**
  `MASI` → Maserati, `SUBN` → Subaru, `MERC` → Mercury. These follow NCIC
  convention, not intuition.
- **Never bulk-replace text in this file.** A refactor once turned
  `"TREK, INC."` into `"TREK.value, INC."` (commit `ae20244`) because the keys
  are strings that look like code.

The CCRS project's `make_map.py` was seeded from this one (42 makers / 84
strings here → 81 / 866 there), so a fix here is usually worth porting.

## Releasing

1. Bump `__version__` in `src/switrs_to_sqlite/__init__.py`. Nothing else
   stores the version.
2. Merge to `main` with `--no-ff`, then create a **lightweight** tag `vX.Y.Z`
   and push the tag.
3. Publish a GitHub release. `release.yml` runs the full CI pipeline, verifies
   the tag matches `__version__`, then publishes to PyPI via trusted
   publishing.

A tag that disagrees with `__version__` fails the release job by design. The
workflow checks out the tag ref, so publishing works before `main` is pushed.

### Deciding whether a change is MAJOR

The operational test: **run the old and new code on the same input. If both
runs succeed and any value or table in the output differs, it is major.**

- A crash does not count — an aborted run produced no database that anything
  could be compatible with.
- CLI-only changes do not count unless they break an existing invocation.
- Additive indices are borderline; treat as minor.

**Pre-tag ritual:** run the previous tag and the release candidate against a
real dump, then diff `sqlite3 <file> .dump` output. An empty diff means
patch/minor. Any diff means the change waits for the next major batch.
Output-changing work is tagged `[v5]`-style in `TODO.md` and batched, so users
absorb one break instead of several.
