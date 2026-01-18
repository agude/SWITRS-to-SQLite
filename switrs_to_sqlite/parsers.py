from collections import OrderedDict
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from switrs_to_sqlite.datatypes import DATATPYE_MAP, DataType
from switrs_to_sqlite.row_types import (
    COLLISION_DATE_TABLE,
    COLLISION_ROW,
    PARTY_ROW,
    VICTIM_ROW,
)


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

    parsing_table: Sequence[Any]
    table_name: str
    has_primary_column: bool
    date_parsing_table: Sequence[tuple[int, str, DataType]] | None
    columns: list[tuple[str, ...]]

    def __init__(
        self,
        parsing_table: Sequence[Any],
        table_name: str,
        has_primary_column: bool,
        date_parsing_table: Sequence[tuple[int, str, DataType]] | None,
    ) -> None:
        """Set up the class and parse the CSV row.

        This method should be called by all derived classes within their own
        __init__() functions, like so:

            super().__init__(row)

        Args:
            row (list): A list of strings containing the information from the
                CSV row, as returned by csv.reader().
        """
        self.parsing_table = parsing_table
        self.table_name = table_name
        self.has_primary_column = has_primary_column
        self.date_parsing_table = date_parsing_table

        self.__datatype_convert = DATATPYE_MAP

        # Set up column names
        self.__set_columns()

    def parse_row(self, row: list[str]) -> list[Any]:
        # The CSV file is malformed, so extend it to avoid KeyErrors
        extended_row = self.__extend_row(row)

        # Set up list of variables for insertion
        values = self.__set_values(extended_row)

        return list(values.values())

    def __set_values(self, row: list[str]) -> OrderedDict[str, Any]:
        """Creates a list of the attributes set in set_variables() in the
        proper order for reading into the SQLite table.

        """
        values: OrderedDict[str, Any] = OrderedDict()
        # If there is no column in the data that is a primary key, than we have
        # to add an automatic first column which needs a NULL inserted
        if not self.has_primary_column:
            values["PRIMARY_COLUMN"] = None

        # Parse each item in the row
        for i_csv, name, datatype, nulls, func, val_map in self.parsing_table:
            dtype = self.__datatype_convert[datatype]

            # Convert the CSV field to a value for SQL using the associated
            # conversion function
            val = func(val=row[i_csv], nulls=nulls, dtype=dtype)

            # If there is a val_map, then use that to convert the value to a
            # return value. This is mainly used to convert "Enums" in the
            # database into human readable values, like 'A' -> 'Stopped'.
            if val_map is not None:
                val = val_map.get(val, val)

            values[name] = val

        # Convert dates as well
        if self.date_parsing_table:
            values["collision_date"] = self.__convert_date(row, "collision_date")
            values["collision_time"] = self.__convert_time(row)
            values["process_date"] = self.__convert_date(row, "process_date")

        return values

    def __convert_date(self, row: list[str], test_name: str) -> str | None:
        # Set up the processing date
        if self.date_parsing_table is None:
            return None
        for i, name, _ in self.date_parsing_table:
            if name == test_name:
                obj = datetime.strptime(row[i], "%Y%m%d")
                return obj.date().isoformat()
        return None

    def __convert_time(self, row: list[str]) -> str | None:
        # Find the correct index for the
        index: int | None = None
        if self.date_parsing_table is None:
            return None
        for i, name, _ in self.date_parsing_table:
            if name == "collision_time":
                index = i
                break

        if index is None:
            return None

        # Set up the collision time
        # 2500 is used as NULL in the source
        collision_time_str = row[index]
        if collision_time_str == "2500":
            time = None
        else:
            # The source data is not always 0 padded, so it will be 900 instead
            # of 0900, and so length 3
            missing_leading_zero_length = 3
            if len(collision_time_str) == missing_leading_zero_length:
                collision_time_str = "0" + collision_time_str

            collision_time_obj = datetime.strptime(collision_time_str, "%H%M")
            time = collision_time_obj.time().isoformat()

        return time

    def __set_columns(self) -> None:
        """Creates a list of column names and types for the SQLite table."""
        self.columns = []
        for i_csv, name, dtype, _, _, _ in self.parsing_table:
            entry: tuple[str, ...] = (name, dtype.value)

            # The first item is special, it is either the "PRIMARY KEY", or we
            # need to add an ID column before it
            if i_csv == 0:
                if self.has_primary_column:
                    entry = (name, dtype.value, "PRIMARY KEY")
                else:
                    zeroth_id_column: tuple[str, ...] = ("id", "INTEGER", "PRIMARY KEY")
                    self.columns.append(zeroth_id_column)

            # Add the entry
            self.columns.append(entry)

        # If we have extra time columns, set those as well
        if self.date_parsing_table:
            for _, name, dtype in self.date_parsing_table:
                self.columns.append((name, dtype.value))

    def __extend_row(self, row: list[str]) -> list[str]:
        """Extend the length of the row attribute with NULL fields.

        Some rows in the CSV are incomplete and are missing columns at the end.
        This function pads these rows with NULLs so they parse correctly.

        """
        # The CSV file is malformed, not ever row is the same length, so we
        # extent it with "" which maps to null in the conversion. The +1
        # converts the final index to length.
        last_index: int = self.parsing_table[-1][0]
        extend = (last_index + 1) - len(row)
        output_row: list[str] = row + extend * [""]  # "" maps to null

        return output_row

    def insert_statement(self, values: list[Any]) -> str:
        """Creates an insert statement used to fill a row in the SQLite
        table."""
        vals = ["?"] * len(values)
        query = "INSERT INTO {table} VALUES ({values})".format(
            table=self.table_name, values=", ".join(vals)
        )

        return query

    def create_table_statement(self) -> str:
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
            table=self.table_name, cols=", ".join(cols)
        )


VictimRow: CSVParser = CSVParser(
    parsing_table=VICTIM_ROW,
    table_name="victims",
    has_primary_column=False,
    date_parsing_table=None,
)


PartyRow: CSVParser = CSVParser(
    parsing_table=PARTY_ROW,
    table_name="parties",
    has_primary_column=False,
    date_parsing_table=None,
)


CollisionRow: CSVParser = CSVParser(
    parsing_table=COLLISION_ROW,
    table_name="collisions",
    has_primary_column=True,
    date_parsing_table=COLLISION_DATE_TABLE,
)
