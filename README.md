# SWITRS-to-SQLite

**Looking to get right to work with the data? Checkout the cleaned dataset on
Kaggle: [California Traffic Collision Data from SWITRS][kaggle]**

[kaggle]: https://www.kaggle.com/alexgude/california-traffic-collision-data-from-switrs

SWITRS-to-SQLite is a Python3 script that will convert the CSV files
provided by the California Highway Patrol's [Statewide Integrated Traffic
Records System (SWITRS)](http://iswitrs.chp.ca.gov/Reports/jsp/userLogin.jsp)
and convert them to an [SQLite3](https://www.sqlite.org/) database.

Instructions to **download the SWITRS data** can be found
[here](requesting_data.md).

## Versioning

This repository follows [Semver][semver]. I will increment the **MAJOR**
version if a change is backwards incompatible for either the Python
command line or the structure of the output database.

[semver]: https://semver.org/

## Installation

The best way to install SWITRS-to-SQLite is with `pip`:

```bash
pip install switrs-to-sqlite
```

This will give you access to the script simply by calling:

```bash
switrs_to_sqlite --help
```

You can also clone this repository:

```bash
git clone https://github.com/agude/SWITRS-to-SQLite.git
cd SWITRS-to-SQLite
./switrs_to_sqlite/switrs_to_sqlite --help
```

If you clone the repository, SWITRS-to-SQLite can be installed as a local
application using the `setup.py` script:

```bash
git clone https://github.com/agude/SWITRS-to-SQLite.git
cd SWITRS-to-SQLite
./setup.py install
```

Which, like using `pip`, will give you access to the script by calling
`switrs_to_sqlite`.

SWITRS-to-SQLite requires only Python3.

## Usage

Using SWITRS-to-SQLite is simple, just point it to the unzipped files from
SWITRS and it will run the conversion:

```bash
switrs_to_sqlite \
CollisionRecords.txt \
PartyRecords.txt \
VictimRecords.txt
```

The script also supports reading `gzip`ed records files:

```bash
switrs_to_sqlite \
CollisionRecords.txt.gz \
PartyRecords.txt.gz \
VictimRecords.txt.gz
```

The conversion process will take about an hour to write the database, which by
default is saved to a file named `switrs.sqlite3`. The output file can be
changed as follows:

```bash
switrs_to_sqlite \
CollisionRecords.txt \
PartyRecords.txt \
VictimRecords.txt \
-o new_db_file.sql
```

The program provides the following help menu when called with `--help`:

```bash
usage: switrs_to_sqlite [-h] [-o OUTPUT_FILE]
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

SWITRS-to-SQLite uses `pytest` to run unit tests (contained in the `tests`
folders). To run the tests, run this command from the base directory:

```bash
python3 -m pytest -v
```
