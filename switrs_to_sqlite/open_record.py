import gzip


def open_record_file(file_name):
    """Open a Record file, even if GZipped.

    Args:
        file_name (str): The name of a file. If the file ends in ".gz" it will
            be read a gzipped file, otherwise it will be assumed to be text.

    """
    if file_name.endswith(".gz"):
        return gzip.open(file_name, "rt")
    return open(file_name, "rt")
