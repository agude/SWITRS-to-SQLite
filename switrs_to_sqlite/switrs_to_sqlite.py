#!/usr/bin/env python3

import argparse
import csv
import sqlite3

from switrs_to_sqlite.open_record import open_record_file
from switrs_to_sqlite.parsers import CollisionRow, PartyRow, VictimRow


# Library version
__version__ = "3.0.12"


def main():
    """Runs the conversion."""

    # We only need to parse command line flags if running as the main script
    argparser = argparse.ArgumentParser(
        description="Convert SWITRS text files to a SQLite3 database"
    )
    # The list of input files
    argparser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
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
        "-o",
        "--output-file",
        help="file to save the database to",
        default="switrs.sqlite3",
    )

    args = argparser.parse_args()

    # Match the parsers with the files they read
    pairs = (
        (CollisionRow, args.collision_record),
        (PartyRow, args.party_record),
        (VictimRow, args.victim_record),
    )

    with sqlite3.connect(args.output_file) as con:
        for RowClass, file_name in pairs:
            # Add the table to the database
            con.execute(RowClass.create_table_statement())

            # Read in the CSV and process each row
            with open_record_file(file_name) as f:
                reader = csv.reader(f)
                next(reader)  # Skip the header

                # Parse each row and insert it into the database
                for row in reader:
                    parsed_row = RowClass.parse_row(row)
                    con.execute(RowClass.insert_statement(parsed_row), parsed_row)


if __name__ == "__main__":
    main()
