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

Or with [UV](https://docs.astral.sh/uv/):

```bash
uv pip install switrs-to-sqlite
```

This will give you access to the script simply by calling:

```bash
switrs_to_sqlite --help
```

### Development Installation

For development, clone the repository and use UV:

```bash
git clone https://github.com/agude/SWITRS-to-SQLite.git
cd SWITRS-to-SQLite
uv sync --dev
```

SWITRS-to-SQLite requires Python 3.10+.

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
usage: switrs_to_sqlite [-h] [--version] [-p {strict,ignore,replace}]
                        [-o OUTPUT_FILE]
                        collision_record party_record victim_record

Convert SWITRS text files to a SQLite3 database

positional arguments:
  collision_record      the CollisionRecords.txt file or the same file gzipped
  party_record          the PartyRecords.txt file or the same file gzipped
  victim_record         the VictimRecords.txt file or the same file gzipped

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -p {strict,ignore,replace}, --parse-error {strict,ignore,replace}
                        how to handle parsing errors
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        file to save the database to
```

## Unit Tests

SWITRS-to-SQLite uses `pytest` to run unit tests (contained in the `tests`
folder). To run the tests:

```bash
uv run pytest -vv
```

Or with [just](https://github.com/casey/just):

```bash
just test
```

Run `just` with no arguments to see all available commands.
