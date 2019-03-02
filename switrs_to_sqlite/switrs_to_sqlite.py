#!/usr/bin/env python3

from datetime import datetime
import argparse
import csv
import sqlite3

from switrs_to_sqlite.converters import convert, negative, string_to_bool
from switrs_to_sqlite.datatypes import DataType, DATATPYE_MAP
from switrs_to_sqlite.open_record import open_record_file
from switrs_to_sqlite.row_types import COLLISION_ROW, PARTY_ROW, VICTIM_ROW


# Library version
__version__ = "1.1.0"


class CSVParser:
    """The base class for all parsing classes.

    Derived classes should define override_parent() to change any
    values. Specifically, they are expected to set table_name and
    members. The members attribute is used to layout the table, determine how
    to insert values, and how to parse the strings in the row attribute.

    Attributes:
        NULLS (list): A list of string values that are always to be considered
            as NULL for all values in the row.
        row (list): A list of strings containing the information from the CSV
            row, as returned by csv.reader().
        table_name (str): The name of the table this parser fills. Used to
            create the table in SQLite.
        has_primary_column (bool): If True, then the first tuple in the members
            attribute is set to a "PRIMARY KEY", otherwise a self-incrementing
            index column is created.
        members (list): A list of tuples indicating how to parse each
            field in the CSV row. The form of each tuple is as follows:
                - int: The position of the field to parse.
                - str: The name to use for the field in the table.
                - DataType: The type to use to store the field value in the
                    table.
                - List OR None: List of additional values to consider NULL.
                    None if no additional values are needed.
                - function: A function to convert the value from the string it
                    is read as to its final form.

        Additional attributes are set based on the names provided in the
        members tuples. They contain the values returned by the function in the
        tuple.

    """

    def __init__(self, parsing_table, table_name, has_primary_column):
        """Set up the class and parse the CSV row.

        This method should be called by all derived classes within their own
        __init__() functions, like so:

            super().__init__(row)

        Args:
            row (list): A list of strings containing the information from the
                CSV row, as returned by csv.reader().
        """
        self.NULLS = ["-", ""]

        self.parsing_table = parsing_table
        self.table_name = table_name
        self.has_primary_column = has_primary_column
        self.__datatype_convert = DATATPYE_MAP

    def parse_row(self, row):
        # The CSV file is malformed, so extend it to avoid KeyErrors
        new_row = self.extend_row(row)

        # Set up list of variables for insertion
        return self.__set_values(row)

    def __set_values(self, row):
        """Creates a list of the attributes set in set_variables() in the
        proper order for reading into the SQLite table.

        """
        values = []
        # If there is no column in the data that is a primary key, than we have
        # to add an automatic first column which needs a NULL inserted
        if self.has_primary_column:
            values.append(None)

        # Parse each item in the row
        for i_csv, name, datatype, nulls, func in self.parsing_table:
            dtype = self.__datatype_convert[datatype]

            # Set up the nulls for this field
            # Must deep copy to prevent polluting the ones stored in the class
            our_nulls = self.NULLS[:]
            if nulls is not None:
                our_nulls += nulls

            # Convert the CSV field to a value for SQL using the associated
            # conversion function
            val = func(val=row[i_csv], nulls=our_nulls, dtype=dtype)

            values.append(val)

        return values

    def set_columns(self):
        """Creates a list of column names and types for the SQLite table."""
        self.columns = []
        for i_csv, name, dtype, _, _ in self.parsing_table:
            entry = (name, dtype.value)
            # The first item is special, it is either the "PRIMARY KEY", or we
            # need to add an ID column before it
            if i_csv == 0:
                if self.has_primary_column:
                    entry = (name, dtype.value, "PRIMARY KEY")
                else:
                    zeroth_id_column = ("id", "INTEGER", "PRIMARY KEY")
                    self.columns.append(zeroth_id_column)

            # Add the entry
            self.columns.append(entry)

    def insert_statement(self):
        """Creates an insert statement used to fill a row in the SQLite table."""
        vals = ['?'] * len(self.values)
        query = "INSERT INTO {table} VALUES ({values})".format(
            table=self.table_name,
            values=", ".join(vals),
        )

        return query

    def create_table_statement(self):
        """Creates a string that can be used to create the correct table in SQLite.

        Use as follows:

            with sqlite3.connect(output_file) as con:
                cursor = con.cursor()
                c = RowClass(row)
                cursor.execute(c.create_table_statement())

        """
        cols = []
        for tup in self.columns:
            cols.append(" ".join(tup))
        return "CREATE TABLE {table} ({cols})".format(
            table=self.table_name,
            cols=", ".join(cols),
        )

    def extend_row(self, row):
        """Extend the length of the row attribute with NULL fields.

        Some rows in the CSV are incomplete and are missing columns at the end.
        This function pads these rows with NULLs so they parse correctly.

        """
        # The CSV file is malformed, not ever row is the same length, so we
        # extent it with "" which maps to null in the conversion. The +1
        # converts the final index to length.
        extend = (self.parsing_table[-1][0] + 1) - len(row)
        row += extend * [""]  # "" maps to null

        return row


VictimRow = CSVParser(
    VICTIM_ROW,
    table_name="Victim",
    has_primary_column=True,
)


PartyRow = CSVParser(
    PARTY_ROW,
    table_name="Party",
    has_primary_column=True,
)


class CollisionRow(CSVRow):
    """Parse CSV rows from the CollisionRecords file.

    This class sets special_members to handle setting up the date fields. It
    uses the method __convert_dates() to fill these fields, and modifies
    set_variables(), set_values(), and set_columns() to add the dates to the
    class objects.

    """

    def __init__(self, row):
        super().__init__(row)

    def override_parent(self):
        self.table_name = "Collision"
        self.has_primary_column = True

        # Set the member variables
        self.members = COLLISION_ROW

        self.special_members = (
            ("Collision_Date", DataType.TEXT),
            ("Collision_Time", DataType.TEXT),
            ("Process_Date", DataType.TEXT),
        )

    def set_variables(self):
        super().set_variables()

        # Set variables that need non-trivial processing
        # self.Collision_Date and self.Collision_Time:
        self.__convert_dates()

    def set_values(self):
        super().set_values()
        for name, _ in self.special_members:
            self.values.append(getattr(self, name))

    def set_columns(self):
        super().set_columns()
        for name, dtype in self.special_members:
            self.columns.append((name, dtype.value))

    def __convert_dates(self):
        """Converts the various date and time fields into two date and one time
        field. """
        # Set up the processing date
        process_obj = datetime.strptime(self.row[2], "%Y%m%d")
        self.Process_Date = process_obj.date().isoformat()

        # Set up the collision date
        collision_obj = datetime.strptime(self.row[4], "%Y%m%d")
        self.Collision_Date = collision_obj.date().isoformat()

        # Set up the collision time
        # 2500 is used as NULL in the source
        collision_time = self.row[5]
        if collision_time == "2500":
            self.Collision_Time = None
        else:
            # The source data is not always 0 padded
            if len(collision_time) == 3:
                collision_time = '0' + collision_time

            collision_time_obj = datetime.strptime(collision_time, "%H%M")
            self.Collision_Time = collision_time_obj.time().isoformat()


def main():
    """Runs the conversion."""

    # We only need to parse command line flags if running as the main script
    argparser = argparse.ArgumentParser(
        description="Convert SWITRS text files to a SQLite3 database"
    )
    # The list of input files
    argparser.add_argument(
        "collision_record",
        type=str,
        help="the CollisionRecords.txt file or the same file gzipped"
    )
    argparser.add_argument(
        "party_record",
        type=str,
        help="the PartyRecords.txt file or the same file gzipped"
    )
    argparser.add_argument(
        "victim_record",
        type=str,
        help="the VictimRecords.txt file or the same file gzipped"
    )
    argparser.add_argument(
        "-o",
        "--output-file",
        help="file to save the database to",
        default="switrs.sqlite3"
    )

    args = argparser.parse_args()

    pairs = (
        (CollisionRow, args.collision_record),
        (PartyRow, args.party_record),
        (VictimRow, args.victim_record),
    )

    with sqlite3.connect(args.output_file) as con:
        cursor = con.cursor()
        for RowClass, file_name in pairs:
            with open_record_file(file_name) as f:
                reader = csv.reader(f)
                # Skip the header
                next(reader)
                added_table = False
                for row in reader:
                    c = RowClass(row)
                    # Add the table the first time
                    if not added_table:
                        cursor.execute(c.create_table_statement())
                        added_table = True

                    # Insert the row
                    cursor.execute(c.insert_statement(), c.values)


if __name__ == "__main__":
    main()
