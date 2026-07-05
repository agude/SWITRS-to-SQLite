from collections.abc import Sequence
from typing import Any

from switrs_to_sqlite.datatypes import DATATYPE_MAP
from switrs_to_sqlite.row_types import (
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
    _prepend_null: bool
    columns: list[tuple[str, ...]]
    _insert_sql: str
    _resolved_indices: dict[str, int]
    _ordered_indices: list[int]
    _max_index: int

    def __init__(
        self,
        parsing_table: Sequence[Column],
        table_name: str,
        has_primary_column: bool,
    ) -> None:
        """Set up the class and parse the CSV row.

        This method should be called by all derived classes within their own
        __init__() functions, like so:

            super().__init__(row)

        Args:
            parsing_table: A sequence of Column objects defining the schema.
            table_name: The name of the SQLite table.
            has_primary_column: Whether the first column is a primary key.
        """
        self.parsing_table = parsing_table
        self.table_name = table_name
        self.has_primary_column = has_primary_column
        self._prepend_null = not has_primary_column
        self._resolved_indices = {}
        self._ordered_indices = []
        self._max_index = 0

        self.__datatype_convert = DATATYPE_MAP

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

        # Pre-calculate max index for row extension (performance optimization:
        # avoid recalculating max() for every row in multi-million row files)
        self._max_index = max(self._resolved_indices.values())

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

        extended_row = self.__extend_row(row)
        return self.__set_values(extended_row)

    def __set_values(self, row: list[str]) -> list[Any]:
        """Build the values list for a single row, ready for SQL insertion."""
        values: list[Any] = []

        if self._prepend_null:
            values.append(None)

        for col, idx in zip(self.parsing_table, self._ordered_indices, strict=True):
            dtype = self.__datatype_convert[col.sql_type]
            val = col.converter(row[idx], dtype, col.nulls)
            if col.mapping is not None:
                val = col.mapping.get(val, val)
            values.append(val)

        return values

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

        col_names = ", ".join(tup[0] for tup in self.columns)
        placeholders = ", ".join("?" * len(self.columns))
        self._insert_sql = (
            f"INSERT INTO {self.table_name} ({col_names}) VALUES ({placeholders})"
        )

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

    def insert_statement(self) -> str:
        """Returns the precomputed INSERT statement for this table."""
        return self._insert_sql

    def create_table_statement(self) -> str:
        """Creates a string that can be used to create the correct table in SQLite.

        Use as follows:

            with sqlite3.connect(output_file) as con:
                cursor = con.cursor()
                c = RowClass(row)
                cursor.execute(c.create_table_statement())

        """
        cols = ", ".join(" ".join(tup) for tup in self.columns)
        return f"CREATE TABLE {self.table_name} ({cols})"


def make_collision_parser() -> CSVParser:
    return CSVParser(
        parsing_table=COLLISION_ROW,
        table_name="collisions",
        has_primary_column=True,
    )


def make_party_parser() -> CSVParser:
    return CSVParser(
        parsing_table=PARTY_ROW,
        table_name="parties",
        has_primary_column=False,
    )


def make_victim_parser() -> CSVParser:
    return CSVParser(
        parsing_table=VICTIM_ROW,
        table_name="victims",
        has_primary_column=False,
    )
