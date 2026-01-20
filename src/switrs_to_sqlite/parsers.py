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
from switrs_to_sqlite.schema import Column


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
        has_primary_column (bool): If True, then the first Column in the
            parsing_table is set to a "PRIMARY KEY", otherwise a self-incrementing
            index column is created.
        parsing_table (Sequence[Column]): A sequence of Column objects defining
            how to parse each field in the CSV row.

        Additional attributes are set based on the names provided in the
        Column objects. They contain the values returned by the converter
        function.

    """

    parsing_table: Sequence[Column]
    table_name: str
    has_primary_column: bool
    date_parsing_table: Sequence[tuple[str, str, DataType]] | None
    columns: list[tuple[str, ...]]
    _resolved_indices: dict[str, int]
    _date_indices: dict[str, int]
    _ordered_indices: list[int]
    # Pre-calculated indices for date columns (avoids iteration/string comparison per row)
    _collision_date_idx: int | None
    _collision_time_idx: int | None
    _process_date_idx: int | None
    _max_index: int

    def __init__(
        self,
        parsing_table: Sequence[Column],
        table_name: str,
        has_primary_column: bool,
        date_parsing_table: Sequence[tuple[str, str, DataType]] | None,
    ) -> None:
        """Set up the class and parse the CSV row.

        This method should be called by all derived classes within their own
        __init__() functions, like so:

            super().__init__(row)

        Args:
            parsing_table: A sequence of Column objects defining the schema.
            table_name: The name of the SQLite table.
            has_primary_column: Whether the first column is a primary key.
            date_parsing_table: Optional date field definitions.
        """
        self.parsing_table = parsing_table
        self.table_name = table_name
        self.has_primary_column = has_primary_column
        self.date_parsing_table = date_parsing_table
        self._resolved_indices = {}
        self._date_indices = {}
        self._ordered_indices = []
        self._collision_date_idx = None
        self._collision_time_idx = None
        self._process_date_idx = None
        self._max_index = 0

        self.__datatype_convert = DATATPYE_MAP

        # Set up column names
        self.__set_columns()

    def resolve_indices(self, header_row: list[str]) -> dict[str, int]:
        """Build header-to-index mapping from CSV header row.

        Handles:
        - BOM stripping from first column
        - Case-insensitive matching (all headers lowercased)

        Args:
            header_row: The first row of the CSV file containing headers.

        Returns:
            The header-to-index mapping for all headers in the file.

        Raises:
            ValueError: If a required column header is missing or duplicated.
        """
        # BOM is handled by open_record_file using utf-8-sig encoding

        # Check for duplicate headers (case-insensitive)
        seen: dict[str, int] = {}
        for i, h in enumerate(header_row):
            normalized = h.lower()
            if normalized in seen:
                raise ValueError(
                    f"Duplicate column header '{h}' at indices {seen[normalized]} and {i}"
                )
            seen[normalized] = i

        # Use the already-built mapping
        header_map = seen

        # Resolve indices for parsing_table columns
        # (col.header is already lowercase via __post_init__)
        self._resolved_indices = {}
        for col in self.parsing_table:
            if col.header not in header_map:
                raise ValueError(f"Missing expected column: {col.header}")
            self._resolved_indices[col.header] = header_map[col.header]

        # Pre-calculate ordered indices aligned with parsing_table for faster
        # row parsing (avoids dict lookup per column per row)
        self._ordered_indices = [
            self._resolved_indices[col.header] for col in self.parsing_table
        ]

        # Resolve indices for date columns (normalize header here too)
        # Also pre-calculate specific indices to avoid iteration in convert methods
        if self.date_parsing_table:
            self._date_indices = {}
            for header, db_name, _ in self.date_parsing_table:
                normalized = header.lower()
                if normalized not in header_map:
                    raise ValueError(f"Missing expected date column: {header}")
                idx = header_map[normalized]
                self._date_indices[normalized] = idx
                # Pre-calculate specific indices for date conversion methods
                if db_name == "collision_date":
                    self._collision_date_idx = idx
                elif db_name == "collision_time":
                    self._collision_time_idx = idx
                elif db_name == "process_date":
                    self._process_date_idx = idx

        # Pre-calculate max index for row extension (performance optimization:
        # avoid recalculating max() for every row in multi-million row files)
        self._max_index = max(self._resolved_indices.values())
        if self._date_indices:
            self._max_index = max(self._max_index, max(self._date_indices.values()))

        return header_map

    def parse_row(self, row: list[str]) -> list[Any]:
        """Parse a CSV row into a list of values for database insertion.

        Args:
            row: A CSV row as a list of strings.

        Returns:
            A list of converted values ready for database insertion.

        Raises:
            RuntimeError: If resolve_indices has not been called first.
        """
        if not self._resolved_indices:
            raise RuntimeError("resolve_indices must be called before parsing rows")

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

        # Parse each item in the row using pre-calculated indices
        for col, idx in zip(self.parsing_table, self._ordered_indices, strict=True):
            dtype = self.__datatype_convert[col.sql_type]

            # Convert the CSV field to a value for SQL using the associated
            # conversion function
            val = col.converter(row[idx], dtype, col.nulls)

            # If there is a mapping, then use that to convert the value to a
            # return value. This is mainly used to convert "Enums" in the
            # database into human readable values, like 'A' -> 'Stopped'.
            if col.mapping is not None:
                val = col.mapping.get(val, val)

            values[col.name] = val

        # Convert dates as well
        if self.date_parsing_table:
            values["collision_date"] = self.__convert_date(row, "collision_date")
            values["collision_time"] = self.__convert_time(row)
            values["process_date"] = self.__convert_date(row, "process_date")

        return values

    def __convert_date(self, row: list[str], date_type: str) -> str | None:
        # Use pre-calculated indices (avoids iteration per row)
        if date_type == "collision_date":
            idx = self._collision_date_idx
        elif date_type == "process_date":
            idx = self._process_date_idx
        else:
            return None

        if idx is None:
            return None

        obj = datetime.strptime(row[idx], "%Y%m%d")
        return obj.date().isoformat()

    def __convert_time(self, row: list[str]) -> str | None:
        # Use pre-calculated index (avoids iteration per row)
        if self._collision_time_idx is None:
            return None

        # Set up the collision time
        # 2500 is used as NULL in the source
        collision_time_str = row[self._collision_time_idx]
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
        is_first = True
        for col in self.parsing_table:
            entry: tuple[str, ...] = (col.name, col.sql_type.value)

            # The first item is special, it is either the "PRIMARY KEY", or we
            # need to add an ID column before it
            if is_first:
                if self.has_primary_column:
                    entry = (col.name, col.sql_type.value, "PRIMARY KEY")
                else:
                    zeroth_id_column: tuple[str, ...] = ("id", "INTEGER", "PRIMARY KEY")
                    self.columns.append(zeroth_id_column)
                is_first = False

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
        # The CSV file is malformed, not every row is the same length, so we
        # extend it with "" which maps to null in the conversion. The +1
        # converts the final index to length.
        # Uses pre-calculated _max_index from resolve_indices() for performance.
        extend = (self._max_index + 1) - len(row)
        if extend > 0:
            return row + [""] * extend
        return row

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
