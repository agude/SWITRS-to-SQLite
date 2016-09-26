# SWITRS-2-SQLite

SWITRS-2-SQLite is a Python3 script that will convert the CSV files
provided by the California Highway Patrol's [Statewide Integrated Traffic
Records System (SWITRS)](http://iswitrs.chp.ca.gov/Reports/jsp/userLogin.jsp)
and convert them to an [SQLite3](https://www.sqlite.org/) database.

Instructions to **download the SWITRS data** can be found
[here](requesting_data.md).

## Installation

To install SWITRS-2-SQLite clone this repository:

```bash
git clone https://github.com/agude/SWITRS-2-SQLite.git
cd SWITRS-2-SQLite
./load_into_database.py --help
```

SWITRS-2-SQLite requires only Python3.

## Usage

Using SWITRS-2-SQLite is simple, just point it to the unzipped files from
SWITRS and it will run the conversion:

```bash
./load_into_database.py \
CollisionRecords.txt \
PartyRecords.txt \
VictimRecords.txt
```

The script also supports reading `gzip`ed records files:

```bash
./load_into_database.py \
CollisionRecords.txt.gz \
PartyRecords.txt.gz \
VictimRecords.txt.gz
```

The conversion process will take about an hour to write the database, which by
default is saved to a file named `switrs.sqlite3`. The output file can be
changed as follows:

```bash
./load_into_database.py \
CollisionRecords.txt \
PartyRecords.txt \
VictimRecords.txt \
-o new_db_file.sql
```

The program provides the following help menu when called with `--help`:

```bash
usage: load_into_database.py [-h] [-o OUTPUT_FILE]
                             collision_record party_record victim_record

Convert SWITRS text files to a SQLite database

positional arguments:
  collision_record      the CollisionRecords.txt file or the same file gzipped
  party_record          the PartyRecords.txt file or the same file gzipped
  victim_record         the VictimRecords.txt file or the same file gzipped

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        file to save the database to
```

## Unit Tests

SWITRS-2-SQLite uses `pytest` to run unit tests (contained in the `tests`
folders). To run the tests, run this command from the base directory:

```bash
python3 -m pytest -v
```
