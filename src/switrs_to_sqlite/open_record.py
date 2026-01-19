import gzip
from typing import TextIO


def open_record_file(file_name: str, errors: str | None = None) -> TextIO:
    """Open a Record file, even if GZipped.

    Args:
        file_name (str): The name of a file. If the file ends in ".gz" it will
            be read a gzipped file, otherwise it will be assumed to be text.

    """
    if file_name.endswith(".gz"):
        return gzip.open(file_name, "rt", errors=errors)
    return open(file_name, errors=errors)
