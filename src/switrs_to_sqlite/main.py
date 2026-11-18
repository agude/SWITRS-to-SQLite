#!/usr/bin/env python3

import argparse
import contextlib
import csv
import sqlite3
import sys
import zlib
from collections.abc import Generator, Iterable, Iterator
from pathlib import Path
from typing import Any

from switrs_to_sqlite import __version__
from switrs_to_sqlite.open_record import open_record_file
from switrs_to_sqlite.parsers import (
    CSVParser,
    make_collision_parser,
    make_party_parser,
    make_victim_parser,
)

_PROGRESS_INTERVAL = 100_000

# ValueError covers bad headers and UnicodeDecodeError. OSError covers
# gzip.BadGzipFile. EOFError is a truncated gzip stream.
_RECORD_FILE_ERRORS = (OSError, EOFError, ValueError, csv.Error, zlib.error)


class RecordFileError(Exception):
    """An input record file could not be read or converted."""


class _RowCounter:
    __slots__ = ("count",)

    def __init__(self) -> None:
        self.count = 0


def _parsed_rows(
    reader: Iterator[list[str]],
    row_parser: CSVParser,
    counter: _RowCounter,
) -> Generator[list[Any], None, None]:
    """Yield parsed rows while printing progress to stderr."""
    table = row_parser.table_name
    print(f"Converting {table}...", file=sys.stderr)
    for row in reader:
        counter.count += 1
        if counter.count % _PROGRESS_INTERVAL == 0:
            print(f"  {counter.count:,} rows", file=sys.stderr, flush=True)
        yield row_parser.parse_row(row)
    print(f"  {table}: {counter.count:,} rows total", file=sys.stderr)


def convert_files(
    collision_file: str,
    party_file: str,
    victim_file: str,
    output_file: str,
    *,
    parse_errors: str | None = None,
) -> None:
    """Convert SWITRS CSV files to a SQLite database.

    Args:
        collision_file: Path to CollisionRecords.txt (or gzipped).
        party_file: Path to PartyRecords.txt (or gzipped).
        victim_file: Path to VictimRecords.txt (or gzipped).
        output_file: Path for the output SQLite database.
        parse_errors: How to handle unicode decoding errors in input files.
            One of 'strict', 'ignore', 'replace', or None (defaults to strict).

    Raises:
        FileNotFoundError: If an input file does not exist.
        FileExistsError: If the output file already exists.
        RecordFileError: If an input file cannot be read or converted. The
            partial output file is removed.
    """
    for input_file in (collision_file, party_file, victim_file):
        if not Path(input_file).exists():
            raise FileNotFoundError(f"Input file not found: '{input_file}'")

    output_path = Path(output_file)
    if output_path.exists():
        raise FileExistsError(
            f"Output file '{output_file}' already exists. Remove it before rerunning."
        )

    record_sources = (
        (make_collision_parser(), collision_file),
        (make_party_parser(), party_file),
        (make_victim_parser(), victim_file),
    )

    # A partial database would block the rerun and could pass for a real one.
    try:
        _write_database(output_file, record_sources, parse_errors)
    except BaseException:
        output_path.unlink(missing_ok=True)
        raise


def _write_database(
    output_file: str,
    record_sources: Iterable[tuple[CSVParser, str]],
    parse_errors: str | None,
) -> None:
    """Create the database and load every record file into it."""
    with contextlib.closing(sqlite3.connect(output_file)) as con, con:
        con.execute("PRAGMA journal_mode = OFF")
        con.execute("PRAGMA synchronous = OFF")
        con.execute("PRAGMA cache_size = -64000")

        for row_parser, file_name in record_sources:
            con.execute(row_parser.create_table_statement())
            try:
                _load_record_file(con, row_parser, file_name, parse_errors)
            except _RECORD_FILE_ERRORS as error:
                raise RecordFileError(f"Could not convert '{file_name}': {error}") from error

        con.execute("CREATE INDEX idx_parties_case_id ON parties (case_id)")
        con.execute("CREATE INDEX idx_victims_case_id ON victims (case_id)")


def _load_record_file(
    con: sqlite3.Connection,
    row_parser: CSVParser,
    file_name: str,
    parse_errors: str | None,
) -> None:
    """Insert every row of one record file into its table."""
    with open_record_file(file_name, errors=parse_errors) as f:
        reader = csv.reader(f)
        try:
            header_row = next(reader)
        except StopIteration:
            print(f"Warning: '{file_name}' is empty, skipping.", file=sys.stderr)
            return

        row_parser.resolve_indices(header_row)

        counter = _RowCounter()
        insert_sql = row_parser.insert_statement()
        con.executemany(insert_sql, _parsed_rows(reader, row_parser, counter))

        if row_parser.has_primary_column:
            cursor = con.execute(f"SELECT COUNT(*) FROM {row_parser.table_name}")
            inserted = cursor.fetchone()[0]
            skipped = counter.count - inserted
            if skipped:
                print(
                    f"Warning: {skipped:,} duplicate case_id rows "
                    f"skipped in {row_parser.table_name}.",
                    file=sys.stderr,
                )


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for SWITRS-to-SQLite conversion."""
    argparser = argparse.ArgumentParser(
        description="Convert SWITRS text files to a SQLite3 database"
    )
    argparser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    argparser.add_argument(
        "collision_record",
        type=str,
        help="the CollisionRecords.txt file or the same file gzipped",
    )
    argparser.add_argument(
        "party_record",
        type=str,
        help="the PartyRecords.txt file or the same file gzipped",
    )
    argparser.add_argument(
        "victim_record",
        type=str,
        help="the VictimRecords.txt file or the same file gzipped",
    )
    argparser.add_argument(
        "-p",
        "--parse-error",
        help=(
            "how to handle unicode decoding errors in input files: "
            "'strict' raises an error (default), "
            "'ignore' skips invalid characters, "
            "'replace' substitutes a replacement character"
        ),
        choices=["strict", "ignore", "replace"],
    )
    argparser.add_argument(
        "-o",
        "--output-file",
        help="file to save the database to",
        default="switrs.sqlite3",
    )

    args = argparser.parse_args(argv)

    try:
        convert_files(
            collision_file=args.collision_record,
            party_file=args.party_record,
            victim_file=args.victim_record,
            output_file=args.output_file,
            parse_errors=args.parse_error,
        )
    except (FileExistsError, FileNotFoundError, RecordFileError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1) from None
    except sqlite3.Error as e:
        print(f"Error: Could not write '{args.output_file}': {e}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
