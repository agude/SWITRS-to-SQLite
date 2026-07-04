import gzip
from pathlib import Path
from typing import TextIO

_GZIP_MAGIC = b"\x1f\x8b"


def open_record_file(file_name: str, errors: str | None = None) -> TextIO:
    """Open a Record file, detecting gzip by magic bytes.

    Args:
        file_name: The name of a file. Gzip files are detected by the
            two-byte magic number, not the file extension.
        errors: How to handle Unicode decoding errors (passed to open/gzip.open).
    """
    path = Path(file_name)
    with path.open("rb") as f:
        magic = f.read(2)

    # Use utf-8-sig to automatically handle BOM if present
    if magic == _GZIP_MAGIC:
        return gzip.open(file_name, "rt", encoding="utf-8-sig", errors=errors)
    return path.open(encoding="utf-8-sig", errors=errors)
