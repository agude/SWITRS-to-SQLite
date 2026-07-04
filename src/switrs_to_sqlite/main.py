#!/usr/bin/env python3

import argparse
import contextlib
import csv
import sqlite3
import sys
from collections.abc import Generator, Iterator
from pathlib import Path
from typing import Any

from switrs_to_sqlite.open_record import open_record_file
from switrs_to_sqlite.parsers import CSVParser, CollisionRow, PartyRow, VictimRow

_PROGRESS_INTERVAL = 100_000

# Library version
__version__: str = "4.5.1"


def _parsed_rows(
    reader: Iterator[list[str]],
    row_parser: CSVParser,
) -> Generator[list[Any], None, None]:
    """Yield parsed rows while printing progress to stderr."""
    table = row_parser.table_name
    print(f"Converting {table}...", file=sys.stderr)
    count = 0
    for row in reader:
        count += 1
        if count % _PROGRESS_INTERVAL == 0:
            print(f"  {count:,} rows", file=sys.stderr, flush=True)
        yield row_parser.parse_row(row)
    print(f"  {table}: {count:,} rows total", file=sys.stderr)


def main(argv: list[str] | None = None) -> None:
    """Runs the conversion.

    Args:
        argv: Command line arguments. If None, uses sys.argv.
    """

    # We only need to parse command line flags if running as the main script
    argparser = argparse.ArgumentParser(
        description="Convert SWITRS text files to a SQLite3 database"
    )
    # The list of input files
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

    output_path = Path(args.output_file)
    if output_path.exists():
        print(
            f"Error: output file '{args.output_file}' already exists. "
            "Remove it before rerunning.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # Match the parsers with the files they read
    pairs = (
        (CollisionRow, args.collision_record),
        (PartyRow, args.party_record),
        (VictimRow, args.victim_record),
    )

    with contextlib.closing(sqlite3.connect(args.output_file)) as con, con:
        con.execute("PRAGMA journal_mode = OFF")
        con.execute("PRAGMA synchronous = OFF")
        con.execute("PRAGMA cache_size = -64000")

        for row_parser, file_name in pairs:
            # Add the table to the database
            con.execute(row_parser.create_table_statement())

            # Read in the CSV and process each row
            with open_record_file(file_name, errors=args.parse_error) as f:
                reader = csv.reader(f)
                try:
                    header_row = next(reader)
                except StopIteration:
                    # Empty file (or only BOM), skip to next file
                    continue

                # Resolve header-to-index mapping once per file
                row_parser.resolve_indices(header_row)

                insert_sql = row_parser.insert_statement()
                con.executemany(insert_sql, _parsed_rows(reader, row_parser))


if __name__ == "__main__":
    main()
