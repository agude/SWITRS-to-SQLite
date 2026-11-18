import gzip
from pathlib import Path
from typing import TextIO

_GZIP_MAGIC = b"\x1f\x8b"
# utf-8-sig also reads files without a BOM.
_RECORD_ENCODING = "utf-8-sig"


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

    if magic == _GZIP_MAGIC:
        return gzip.open(file_name, "rt", encoding=_RECORD_ENCODING, errors=errors)
    return path.open(encoding=_RECORD_ENCODING, errors=errors)
