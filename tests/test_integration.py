"""Integration tests for SWITRS to SQLite conversion.

Tests end-to-end conversion of raw SWITRS CSV data to SQLite database,
comparing output against a golden snapshot file.
"""

import json
import sqlite3
from pathlib import Path

from switrs_to_sqlite.main import main

# Paths
DATA_DIR = Path(__file__).parent / "data"
GOLDEN_SNAPSHOT = DATA_DIR / "golden_snapshot.json"

# Headers (kept inline as they're needed to create valid input files)
COLLISIONS_HEADER = "CASE_ID,ACCIDENT_YEAR,PROC_DATE,JURIS,COLLISION_DATE,COLLISION_TIME,OFFICER_ID,REPORTING_DISTRICT,DAY_OF_WEEK,CHP_SHIFT,POPULATION,CNTY_CITY_LOC,SPECIAL_COND,BEAT_TYPE,CHP_BEAT_TYPE,CITY_DIVISION_LAPD,CHP_BEAT_CLASS,BEAT_NUMBER,PRIMARY_RD,SECONDARY_RD,DISTANCE,DIRECTION,INTERSECTION,WEATHER_1,WEATHER_2,STATE_HWY_IND,CALTRANS_COUNTY,CALTRANS_DISTRICT,STATE_ROUTE,ROUTE_SUFFIX,POSTMILE_PREFIX,POSTMILE,LOCATION_TYPE,RAMP_INTERSECTION,SIDE_OF_HWY,TOW_AWAY,COLLISION_SEVERITY,NUMBER_KILLED,NUMBER_INJURED,PARTY_COUNT,PRIMARY_COLL_FACTOR,PCF_CODE_OF_VIOL,PCF_VIOL_CATEGORY,PCF_VIOLATION,PCF_VIOL_SUBSECTION,HIT_AND_RUN,TYPE_OF_COLLISION,MVIW,PED_ACTION,ROAD_SURFACE,ROAD_COND_1,ROAD_COND_2,LIGHTING,CONTROL_DEVICE,CHP_ROAD_TYPE,PEDESTRIAN_ACCIDENT,BICYCLE_ACCIDENT,MOTORCYCLE_ACCIDENT,TRUCK_ACCIDENT,NOT_PRIVATE_PROPERTY,ALCOHOL_INVOLVED,STWD_VEHTYPE_AT_FAULT,CHP_VEHTYPE_AT_FAULT,COUNT_SEVERE_INJ,COUNT_VISIBLE_INJ,COUNT_COMPLAINT_PAIN,COUNT_PED_KILLED,COUNT_PED_INJURED,COUNT_BICYCLIST_KILLED,COUNT_BICYCLIST_INJURED,COUNT_MC_KILLED,COUNT_MC_INJURED,PRIMARY_RAMP,SECONDARY_RAMP,LATITUDE,LONGITUDE"
PARTIES_HEADER = "CASE_ID,PARTY_NUMBER,PARTY_TYPE,AT_FAULT,PARTY_SEX,PARTY_AGE,PARTY_SOBRIETY,PARTY_DRUG_PHYSICAL,DIR_OF_TRAVEL,PARTY_SAFETY_EQUIP_1,PARTY_SAFETY_EQUIP_2,FINAN_RESPONS,SP_INFO_1,SP_INFO_2,SP_INFO_3,OAF_VIOLATION_CODE,OAF_VIOL_CAT,OAF_VIOL_SECTION,OAF_VIOLATION_SUFFIX,OAF_1,OAF_2,PARTY_NUMBER_KILLED,PARTY_NUMBER_INJURED,MOVE_PRE_ACC,VEHICLE_YEAR,VEHICLE_MAKE,STWD_VEHICLE_TYPE,CHP_VEH_TYPE_TOWING,CHP_VEH_TYPE_TOWED,RACE,INATTENTION,SPECIAL_INFO_F,SPECIAL_INFO_G"
VICTIMS_HEADER = "CASE_ID,PARTY_NUMBER,VICTIM_ROLE,VICTIM_SEX,VICTIM_AGE,VICTIM_DEGREE_OF_INJURY,VICTIM_SEATING_POSITION,VICTIM_SAFETY_EQUIP_1,VICTIM_SAFETY_EQUIP_2,VICTIM_EJECTED"


def load_golden_data() -> dict:
    """Load expected data from golden snapshot JSON file."""
    with open(GOLDEN_SNAPSHOT) as f:
        return json.load(f)


def test_end_to_end(tmp_path: Path) -> None:
    """Test complete conversion pipeline against golden snapshot."""
    # Set up paths
    collisions_path = tmp_path / "collisions.txt"
    parties_path = tmp_path / "parties.txt"
    victims_path = tmp_path / "victims.txt"
    db_path = tmp_path / "switrs.sqlite3"

    # Read raw data from tests/data/
    collisions_data = (DATA_DIR / "test_collisions.txt").read_text()
    parties_data = (DATA_DIR / "test_parties.txt").read_text()
    victims_data = (DATA_DIR / "test_victims.txt").read_text()

    # Write input CSVs with headers
    collisions_path.write_text(COLLISIONS_HEADER + "\n" + collisions_data)
    parties_path.write_text(PARTIES_HEADER + "\n" + parties_data)
    victims_path.write_text(VICTIMS_HEADER + "\n" + victims_data)

    # Run conversion using dependency injection
    main(
        [
            str(collisions_path),
            str(parties_path),
            str(victims_path),
            "-o",
            str(db_path),
        ]
    )

    # Verify database was created
    assert db_path.exists(), "Database file was not created"

    # Load golden data
    expected_data = load_golden_data()

    # Connect and verify
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        for table_name, expected_content in expected_data.items():
            expected_columns = expected_content["columns"]
            expected_rows = expected_content["rows"]

            # Check columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            actual_columns = [info[1] for info in cursor.fetchall()]

            assert actual_columns == expected_columns, (
                f"Columns for table '{table_name}' do not match golden data.\n"
                f"Expected: {expected_columns}\n"
                f"Actual:   {actual_columns}"
            )

            # Check rows (ordered by primary key for stability)
            sort_col = "id" if "id" in actual_columns else "case_id"
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY {sort_col}")
            actual_rows = cursor.fetchall()

            # Assert row count matches
            assert len(actual_rows) == len(expected_rows), (
                f"Row count for table '{table_name}' does not match.\n"
                f"Expected: {len(expected_rows)}\n"
                f"Actual:   {len(actual_rows)}"
            )

            # Assert content (convert JSON arrays to tuples for comparison)
            for i, (actual_row, expected_row) in enumerate(
                zip(actual_rows, expected_rows, strict=True)
            ):
                expected_tuple = tuple(expected_row)
                assert actual_row == expected_tuple, (
                    f"Row {i} in table '{table_name}' does not match golden data.\n"
                    f"Expected: {expected_tuple}\n"
                    f"Actual:   {actual_row}"
                )
    finally:
        conn.close()
