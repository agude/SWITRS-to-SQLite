from enum import Enum, unique


@unique
class DataType(Enum):
    """A class used to encode the types allowed in SQLite."""

    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"
    NULL = "NULL"


# Conversion from SQLite data types to Python data types
DATATPYE_MAP = {
    DataType.INTEGER: int,
    DataType.REAL: float,
    DataType.TEXT: str,
    DataType.BLOB: str,
    DataType.NULL: None,
}
