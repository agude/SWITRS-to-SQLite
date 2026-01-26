# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SWITRS-to-SQLite converts California Highway Patrol SWITRS (Statewide Integrated Traffic Records System) CSV files into an SQLite database. It processes three input files: CollisionRecords, PartyRecords, and VictimRecords.

## Commands

```bash
# Install dependencies
uv sync --dev

# Run tests
just test                    # or: uv run pytest -vv
just test tests/test_converters.py  # single file
just test -k "test_name"     # single test by name

# Lint and format
just lint                    # check for lint errors
just lint-fix                # auto-fix lint errors
just format                  # format code
just type-check              # run mypy

# Run all checks (CI equivalent)
just check

# Build package
just build

# Run CLI
uv run switrs_to_sqlite --help
```

## Architecture

### Data Flow

1. `main.py` orchestrates: opens files, creates tables, iterates CSV rows
2. `open_record.py` handles file opening (plain text or gzip, with BOM handling via utf-8-sig)
3. `parsers.py` contains `CSVParser` class and three parser instances: `CollisionRow`, `PartyRow`, `VictimRow`
4. For each file, `resolve_indices()` is called once with the header row to build column index mappings
5. `parse_row()` converts each CSV row using the column definitions

### Column Definition System

Columns are defined as `Column` dataclasses in `row_types.py`. Each column specifies:
- `header`: CSV column name (auto-lowercased)
- `name`: SQLite column name
- `sql_type`: `DataType` enum (TEXT, INTEGER, REAL)
- `nulls`: Set of strings to treat as NULL
- `converter`: Function from `converters.py` to transform values
- `mapping`: Optional dict to translate codes to human-readable values (defined in `value_maps.py`)

### Key Files

- `src/switrs_to_sqlite/row_types.py`: Column definitions for all three record types (COLLISION_ROW, PARTY_ROW, VICTIM_ROW)
- `src/switrs_to_sqlite/parsers.py`: CSVParser class and the three parser instances
- `src/switrs_to_sqlite/converters.py`: Value conversion functions (convert, string_to_bool, negative, etc.)
- `src/switrs_to_sqlite/value_maps.py`: Code-to-value translation dictionaries
- `src/switrs_to_sqlite/schema.py`: Column dataclass definition

### Testing

Tests use fixtures in `conftest.py` that call `resolve_indices()` with header lists matching actual SWITRS CSV column order. Test data lists in `test_*row.py` files must maintain the same column order as these headers.

## Versioning

The project follows SemVer. MAJOR version bumps indicate backwards-incompatible changes to the CLI or database structure. Version is defined in `main.py` as `__version__`.
