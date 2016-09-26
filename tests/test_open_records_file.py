#!/usr/bin/env python3

from load_into_database import open_record_file
import gzip
import pytest


def test_read_gzipped_file(tmpdir):
    # Write a file to read back
    f = tmpdir.join("test.csv.gz")
    contents = "Test contents\nsecond line"
    file_path = f.dirname + "/" + f.basename
    with gzip.open(file_path, 'wt') as f:
        f.write(contents)

    # Read back the file
    with open_record_file(file_path) as f:
        assert f.read() == contents


def test_read_normal_file(tmpdir):
    # Write a file to read back
    f = tmpdir.join("test.csv")
    contents = "Test contents\nsecond line"
    f.write(contents)
    file_path = f.dirname + "/" + f.basename

    # Read back the file
    with open_record_file(file_path) as f:
        assert f.read() == contents