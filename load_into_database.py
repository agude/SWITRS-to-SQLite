#!/usr/bin/env python3

from datetime import datetime
from enum import Enum, unique
import gzip


@unique
class DataType(Enum):
    """A class used to encode the types allowed in SQLite."""
    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"
    NULL = "NULL"


def convert(**kwargs):
    """Convert a value to a dtype, but turn certain values to None.

    Convert calls val.strip() before performing any other work.

    Args:
        **kwargs: Two specific keywords must be passed, a third is optional:
            - val (str): A value to convert to dtype.
            - dtype (callable): A callable object that returns the desired
                type, if None then the val is passed through unchanged.
            - nulls (iterable, optional): An iterable containing strings to check
                against. If val if found to be equal to a string in this list,
                None is returned.

    Returns:
        converted_val: Returns dtype(val) if val is not in nulls, otherwise
            None. If dtype(val) raises a ValueError, None is returned.
    """
    # Get the arguments
    val = kwargs.get("val")
    dtype = kwargs.get("dtype")
    nulls = kwargs.get("nulls", None)

    # Strip spaces
    sval = val.strip()

    # Return None if the val matches a string in nulls
    if nulls is not None:
        if sval in nulls:
            return None

    # Otherwise return the converted value
    if dtype is not None:
        try:
            return dtype(sval)
        except ValueError:
            return None
    # Note: val and not sval because this is the identity operation
    else:
        return val


def negative(**kwargs):
    """Use convert() to convert a value, and then return it multiplied by -1.

    This function uses convert() to perform the conversion and so passes
    through all arguments. If convert() returns None, than this function will
    also.

    Args:
        **kwargs: Two specific keywords must be passed, a third is optional:
            - val (str): A value to convert to dtype.
            - dtype (callable): A callable object that returns the desired
                type, if None then the val is passed through unchanged. The
                returned object should allow multiplication by -1, or None will
                be returned instead.
            - nulls (iterable, optional): An iterable containing strings to check
                against. If val if found to be equal to a string in this list,
                None is returned.

    Returns:
        converted_val: Returns -1 * convert(kwargs), unless convert() returns
            None, in which case None is returned.
    """
    # Use convert to do the conversion
    out_val = convert(**kwargs)

    # If convert succeeded, return the value times -1
    if out_val is not None:
        return -1 * out_val

    return None


def string_to_bool(**kwargs):
    """Convert Y/N or y/n to a True/False, or None if in a list of nulls.

    Args:
        **kwargs: One specific keywords must be passed, a second is optional:
            - val (str): A value to convert to a bool.
            - nulls (iterable, optional): An iterable containing strings to check
                against. If val if found to be equal to a string in this list,
                None is returned.

    Returns:
        converted_val: Returns a bool if val is not in nulls, otherwise None.

    """
    # Get the arguments
    val = kwargs.get("val")
    nulls = kwargs.get("nulls", None)

    # Return None if the val matches a string in nulls
    if nulls is not None:
        if val in nulls:
            return None

    # Check if val is True, otherwise return False
    if val.lower() == "y":
        return True
    return False


class CSVRow(object):
    """The base class for all row parsing classes.

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

    def __init__(self, row):
        """Set up the class and parse the CSV row.

        This method should be called by all derived classes within their own
        __init__() functions, like so:

            super().__init__(row)

        Args:
            row (list): A list of strings containing the information from the
                CSV row, as returned by csv.reader().
        """
        self.NULLS = ["-", ""]
        self.row = row
        self.table_name = None
        self.members = None
        self.has_primary_column = False
        self.__datatype_convert = {
            DataType.INTEGER: int,
            DataType.REAL: float,
            DataType.TEXT: str,
            DataType.BLOB: str,
            DataType.NULL: None,
        }

        self.override_parent()

        if self.members is not None:
            # The CSV file is malformed, so extend it to avoid KeyErrors
            self.extend_row()

            # Set up list of variables for insertion
            self.set_variables()
            self.set_values()
            self.set_columns()

    def override_parent(self):
        """Called before any class logic is executed, should be defined by
        derived classes.

        At a minimum, table_name and members should be defined here.

        """
        pass

    def set_variables(self):
        """Set attributes and convert CSV values using the names and functions
        defined in members.

        """
        for i_csv, name, datatype, nulls, func in self.members:
            dtype = self.__datatype_convert[datatype]

            # Set up the nulls for this field
            # Must deep copy to prevent polluting the ones stored in the class
            our_nulls = self.NULLS[:]
            if nulls is not None:
                our_nulls += nulls

            # Convert the CSV field to a value for SQL
            val = func(val=self.row[i_csv], nulls=our_nulls, dtype=dtype)

            setattr(self, name, val)

    def set_values(self):
        """Creates a list of the attributes set in set_variables() in the
        proper order for reading into the SQLite table.

        """
        self.values = []
        # If there is no column in the data that is a primary key, than we have
        # an automatic first column which needs a NULL inserted to increment.
        if not self.has_primary_column:
            self.values.append(None)
        for _, name, _, _, _ in self.members:
            self.values.append(getattr(self, name))

    def set_columns(self):
        """Creates a list of column names and types for the SQLite table."""
        self.columns = []
        for i_csv, name, dtype, _, _ in self.members:
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

    def extend_row(self):
        """Extend the length of the row attribute with NULL fields.

        Some rows in the CSV are incomplete and are missing columns at the end.
        This function pads these rows with NULLs so they parse correctly.

        """
        # The CSV file is malformed, not ever row is the same length, so we
        # extent it with "" which maps to null in the conversion. The +1
        # converts the final index to length.
        extend = (self.members[-1][0] + 1) - len(self.row)
        self.row += extend * [""]  # "" maps to null


class VictimRow(CSVRow):
    """Parse CSV rows from the VictimRecords file."""

    def __init__(self, row):
        super().__init__(row)

    def override_parent(self):
        self.table_name = "Victim"

        # Set the member variables
        self.members = (
            (0, "Case_ID", DataType.TEXT, None, convert),
            (1, "Party_Number", DataType.INTEGER, None, convert),
            (2, "Victim_Role", DataType.TEXT, None, convert),
            (3, "Victim_Sex", DataType.TEXT, None, convert),
            (4, "Victim_Age", DataType.INTEGER, ["998"], convert),
            (5, "Victim_Degree_Of_Injury", DataType.TEXT, None, convert),
            (6, "Victim_Seating_Position", DataType.TEXT, None, convert),
            (7, "Victim_Safety_Equipment_1", DataType.TEXT, None, convert),
            (8, "Victim_Safety_Equipment_2", DataType.TEXT, None, convert),
            (9, "Victim_Ejected", DataType.TEXT, None, convert),
        )


class PartyRow(CSVRow):
    """Parse CSV rows from the PartyRecords file."""

    def __init__(self, row):
        super().__init__(row)

    def override_parent(self):
        self.table_name = "Party"

        # Set the member variables
        self.members = (
            (0, "Case_ID", DataType.TEXT, None, convert),
            (1, "Party_Number", DataType.INTEGER, None, convert),
            (2, "Party_Type", DataType.TEXT, None, convert),
            (3, "At_Fault", DataType.TEXT, None, string_to_bool),
            (4, "Party_Sex", DataType.TEXT, None, convert),
            (5, "Party_Age", DataType.INTEGER, ["998"], convert),
            (6, "Party_Sobriety", DataType.TEXT, None, convert),
            (7, "Party_Drug_Physical", DataType.TEXT, None, convert),
            (8, "Direction_Of_Travel", DataType.TEXT, None, convert),
            (9, "Party_Safety_Equipment_1", DataType.TEXT, None, convert),
            (10, "Party_Safety_Equipment_2", DataType.TEXT, None, convert),
            (11, "Financial_Responsibility", DataType.TEXT, None, convert),
            (12, "Hazardous_Materials", DataType.TEXT, None, convert),
            (13, "Cellphone_Use", DataType.TEXT, None, convert),
            (14, "School_Bus_Related", DataType.TEXT, None, convert),
            (15, "OAF_Violation_Code", DataType.TEXT, None, convert),
            (16, "OAF_Violation_Category", DataType.TEXT, ["00"], convert),
            (17, "OAF_Violation_Section", DataType.INTEGER, None, convert),
            (18, "OAF_Violation_Suffix", DataType.TEXT, None, convert),
            (19, "Other_Associate_Factor_1", DataType.TEXT, None, convert),
            (20, "Other_Associate_Factor_2", DataType.TEXT, None, convert),
            (21, "Party_Number_Killed", DataType.INTEGER, None, convert),
            (22, "Party_Number_Injured", DataType.INTEGER, None, convert),
            (23, "Movement_Preceding_Collision", DataType.TEXT, None, convert),
            (24, "Vehicle_Year", DataType.INTEGER, ["9999"], convert),
            (25, "Vehicle_Make", DataType.TEXT, None, convert),
            (26, "Statewide_Vehicle_Type", DataType.TEXT, None, convert),
            (27, "CHP_Vehicle_Type_Towing", DataType.TEXT, ["99"], convert),
            (28, "CHP_Vehicle_Type_Towed", DataType.TEXT, ["99"], convert),
            (29, "Party_Race", DataType.TEXT, None, convert),
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
        self.members = (
            (0, "Case_ID", DataType.TEXT, None, convert),
            (3, "Jurisdiction", DataType.INTEGER, None, convert),
            (6, "Officer_ID", DataType.TEXT, None, convert),
            (7, "Reporting_District", DataType.TEXT, None, convert),
            (9, "CHP_Shift", DataType.TEXT, None, convert),
            (10, "Population", DataType.TEXT, None, convert),
            (11, "County_City_Location", DataType.TEXT, None, convert),
            (12, "Special_Condition", DataType.TEXT, None, convert),
            (13, "Beat_Type", DataType.TEXT, None, convert),
            (14, "CHP_Beat_Type", DataType.TEXT, None, convert),
            (15, "City_Division_LAPD", DataType.TEXT, ['0'], convert),
            (16, "CHP_Beat_Class", DataType.TEXT, None, convert),
            (17, "Beat_Number", DataType.TEXT, None, convert),
            (18, "Primary_Road", DataType.TEXT, None, convert),
            (19, "Secondary_Road", DataType.TEXT, None, convert),
            (20, "Distance", DataType.REAL, None, convert),
            (21, "Direction", DataType.TEXT, None, convert),
            (22, "Intersection", DataType.TEXT, None, string_to_bool),
            (23, "Weather_1", DataType.TEXT, None, convert),
            (24, "Weather_2", DataType.TEXT, None, convert),
            (25, "State_Highway_Indicator", DataType.INTEGER, None, string_to_bool),
            (26, "Caltrans_County", DataType.TEXT, None, convert),
            (27, "Caltrans_District", DataType.INTEGER, None, convert),
            (28, "State_Route", DataType.INTEGER, None, convert),
            (29, "Route_Suffix", DataType.TEXT, None, convert),
            (30, "Postmile_Prefix", DataType.TEXT, None, convert),
            (31, "Postmile", DataType.REAL, None, convert),
            (32, "Location_Type", DataType.TEXT, None, convert),
            (33, "Ramp_Intersection", DataType.INTEGER, None, convert),
            (34, "Side_Of_Highway", DataType.TEXT, None, convert),
            (35, "Tow_Away", DataType.INTEGER, None, string_to_bool),
            (36, "Collision_Severity", DataType.INTEGER, None, convert),
            (37, "Killed_Victims", DataType.INTEGER, None, convert),
            (38, "Injured_Victims", DataType.INTEGER, None, convert),
            (39, "Party_Count", DataType.INTEGER, None, convert),
            (40, "Primary_Collision_Factor", DataType.TEXT, None, convert),
            (41, "PCF_Violation_Code", DataType.TEXT, None, convert),
            (42, "PCF_Violation_Category", DataType.TEXT, None, convert),
            (43, "PCF_Violation", DataType.INTEGER, None, convert),
            (44, "PCF_Violation_Subsection", DataType.TEXT, None, convert),
            (45, "Hit_And_Run", DataType.TEXT, None, convert),
            (46, "Type_Of_Collision", DataType.TEXT, None, convert),
            (47, "Motor_Vehicle_Involved_With", DataType.TEXT, None, convert),
            (48, "Ped_Action", DataType.TEXT, None, convert),
            (49, "Road_Surface", DataType.TEXT, None, convert),
            (50, "Road_Condition_1", DataType.TEXT, None, convert),
            (51, "Road_Condition_2", DataType.TEXT, None, convert),
            (52, "Lighting", DataType.TEXT, None, convert),
            (53, "Control_Device", DataType.TEXT, None, convert),
            (54, "CHP_Road_Type", DataType.TEXT, None, convert),
            (55, "Pedestrian_Collision", DataType.INTEGER, None, string_to_bool),
            (56, "Bicycle_Collision", DataType.INTEGER, None, string_to_bool),
            (57, "Motorcycle_Collision", DataType.INTEGER, None, string_to_bool),
            (58, "Truck_Collision", DataType.INTEGER, None, string_to_bool),
            (59, "Not_Private_Property", DataType.INTEGER, None, string_to_bool),
            (60, "Alcohol_Involved", DataType.INTEGER, None, string_to_bool),
            (61, "Statewide_Vehicle_Type_At_Fault", DataType.TEXT, None, convert),
            (62, "CHP_Vehicle_Type_At_Fault", DataType.TEXT, ["99"], convert),
            (63, "Severe_Injury_Count", DataType.INTEGER, None, convert),
            (64, "Other_Visible_Injury_Count", DataType.INTEGER, None, convert),
            (65, "Complaint_Of_Pain_Injury_Count", DataType.INTEGER, None, convert),
            (66, "Pedestrian_Killed_Count", DataType.INTEGER, None, convert),
            (67, "Pedestrian_Injured_Count", DataType.INTEGER, None, convert),
            (68, "Bicyclist_Killed_Count", DataType.INTEGER, None, convert),
            (69, "Bicyclist_Injured_Count", DataType.INTEGER, None, convert),
            (70, "Motorcyclist_Killed_Count", DataType.INTEGER, None, convert),
            (71, "Motorcyclist_Injured_Count", DataType.INTEGER, None, convert),
            (72, "Primary_Ramp", DataType.TEXT, None, convert),
            (73, "Secondary_Ramp", DataType.TEXT, None, convert),
            (74, "Latitude", DataType.REAL, None, convert),
            (75, "Longitude", DataType.REAL, None, negative),
        )

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


def open_record_file(file_name):
    """Open a Record file, even if GZipped.

    Args:
        file_name (str): The name of a file. If the file ends in ".gz" it will
            be read a gzipped file, otherwise it will be assumed to be text.

    """
    if file_name.endswith(".gz"):
        return gzip.open(file_name, "rt")
    return open(file_name, "rt")


if __name__ == "__main__":
    # We only need to parse command line flags if running as the main script
    import argparse

    import csv
    import sqlite3

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
