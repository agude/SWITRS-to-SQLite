__version__: str = "5.2.0"

from switrs_to_sqlite.main import OutputFileError, RecordFileError, convert_files

__all__ = ["OutputFileError", "RecordFileError", "__version__", "convert_files"]
