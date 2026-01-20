"""Schema definitions for CSV-to-database column mappings."""

from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from typing import Any

from switrs_to_sqlite.datatypes import DataType

# Type alias for the converter function signature
ConverterFunc = Callable[
    [str, type[int] | type[float] | type[str] | None, Collection[str] | None],
    Any,
]


def _get_default_converter() -> ConverterFunc:
    """Lazy import to avoid circular dependency."""
    from switrs_to_sqlite.converters import identity

    return identity


@dataclass(frozen=True)
class Column:
    """Schema definition for a single CSV-to-database column mapping.

    Attributes:
        header: The CSV header name (auto-normalized to lowercase).
        name: The name to use for the field in the database table.
        sql_type: The SQLite data type for this column.
        nulls: Collection of string values that should be converted to NULL.
        converter: Function to convert the raw CSV string to its final form.
            Defaults to identity (pass-through).
        mapping: Mapping to transform values (e.g., codes to human-readable strings).
    """

    header: str
    name: str
    sql_type: DataType
    nulls: Collection[str] | None = None
    converter: ConverterFunc = field(default_factory=_get_default_converter)
    mapping: Mapping[str, str | None] | None = None

    def __post_init__(self) -> None:
        """Normalize header to lowercase."""
        # Frozen dataclass requires object.__setattr__
        object.__setattr__(self, "header", self.header.lower())
