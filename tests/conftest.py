"""Shared test fixtures for SWITRS-to-SQLite tests."""

import pytest

from switrs_to_sqlite.parsers import CollisionRow, PartyRow, VictimRow

# Headers matching the actual SWITRS CSV files. These are in the order they
# appear in the actual SWITRS data files from CHP.
#
# IMPORTANT: These header lists must match the column order of the raw data
# lists defined in tests/test_*row.py. The header order determines which
# index each column maps to via resolve_indices(). If SWITRS changes their
# CSV column order in the future, do NOT simply reorder these headers to
# match the new file format - you must also reorder the corresponding test
# data lists in test_collisionrow.py, test_partyrow.py, and test_victimrow.py.

COLLISION_HEADER = [
    "CASE_ID",
    "ACCIDENT_YEAR",
    "PROC_DATE",
    "JURIS",
    "COLLISION_DATE",
    "COLLISION_TIME",
    "OFFICER_ID",
    "REPORTING_DISTRICT",
    "DAY_OF_WEEK",
    "CHP_SHIFT",
    "POPULATION",
    "CNTY_CITY_LOC",
    "SPECIAL_COND",
    "BEAT_TYPE",
    "CHP_BEAT_TYPE",
    "CITY_DIVISION_LAPD",
    "CHP_BEAT_CLASS",
    "BEAT_NUMBER",
    "PRIMARY_RD",
    "SECONDARY_RD",
    "DISTANCE",
    "DIRECTION",
    "INTERSECTION",
    "WEATHER_1",
    "WEATHER_2",
    "STATE_HWY_IND",
    "CALTRANS_COUNTY",
    "CALTRANS_DISTRICT",
    "STATE_ROUTE",
    "ROUTE_SUFFIX",
    "POSTMILE_PREFIX",
    "POSTMILE",
    "LOCATION_TYPE",
    "RAMP_INTERSECTION",
    "SIDE_OF_HWY",
    "TOW_AWAY",
    "COLLISION_SEVERITY",
    "NUMBER_KILLED",
    "NUMBER_INJURED",
    "PARTY_COUNT",
    "PRIMARY_COLL_FACTOR",
    "PCF_CODE_OF_VIOL",
    "PCF_VIOL_CATEGORY",
    "PCF_VIOLATION",
    "PCF_VIOL_SUBSECTION",
    "HIT_AND_RUN",
    "TYPE_OF_COLLISION",
    "MVIW",
    "PED_ACTION",
    "ROAD_SURFACE",
    "ROAD_COND_1",
    "ROAD_COND_2",
    "LIGHTING",
    "CONTROL_DEVICE",
    "CHP_ROAD_TYPE",
    "PEDESTRIAN_ACCIDENT",
    "BICYCLE_ACCIDENT",
    "MOTORCYCLE_ACCIDENT",
    "TRUCK_ACCIDENT",
    "NOT_PRIVATE_PROPERTY",
    "ALCOHOL_INVOLVED",
    "STWD_VEHTYPE_AT_FAULT",
    "CHP_VEHTYPE_AT_FAULT",
    "COUNT_SEVERE_INJ",
    "COUNT_VISIBLE_INJ",
    "COUNT_COMPLAINT_PAIN",
    "COUNT_PED_KILLED",
    "COUNT_PED_INJURED",
    "COUNT_BICYCLIST_KILLED",
    "COUNT_BICYCLIST_INJURED",
    "COUNT_MC_KILLED",
    "COUNT_MC_INJURED",
    "PRIMARY_RAMP",
    "SECONDARY_RAMP",
    "LATITUDE",
    "LONGITUDE",
]

PARTY_HEADER = [
    "CASE_ID",
    "PARTY_NUMBER",
    "PARTY_TYPE",
    "AT_FAULT",
    "PARTY_SEX",
    "PARTY_AGE",
    "PARTY_SOBRIETY",
    "PARTY_DRUG_PHYSICAL",
    "DIR_OF_TRAVEL",
    "PARTY_SAFETY_EQUIP_1",
    "PARTY_SAFETY_EQUIP_2",
    "FINAN_RESPONS",
    "SP_INFO_1",
    "SP_INFO_2",
    "SP_INFO_3",
    "OAF_VIOLATION_CODE",
    "OAF_VIOL_CAT",
    "OAF_VIOL_SECTION",
    "OAF_VIOLATION_SUFFIX",
    "OAF_1",
    "OAF_2",
    "PARTY_NUMBER_KILLED",
    "PARTY_NUMBER_INJURED",
    "MOVE_PRE_ACC",
    "VEHICLE_YEAR",
    "VEHICLE_MAKE",
    "STWD_VEHICLE_TYPE",
    "CHP_VEH_TYPE_TOWING",
    "CHP_VEH_TYPE_TOWED",
    "RACE",
]

VICTIM_HEADER = [
    "CASE_ID",
    "PARTY_NUMBER",
    "VICTIM_ROLE",
    "VICTIM_SEX",
    "VICTIM_AGE",
    "VICTIM_DEGREE_OF_INJURY",
    "VICTIM_SEATING_POSITION",
    "VICTIM_SAFETY_EQUIP_1",
    "VICTIM_SAFETY_EQUIP_2",
    "VICTIM_EJECTED",
]


@pytest.fixture(autouse=True)
def resolve_parser_indices() -> None:
    """Resolve header-to-index mappings for all parsers before each test.

    This fixture runs automatically before every test to ensure the parsers
    have their indices resolved, which is required for parse_row() to work.
    """
    CollisionRow.resolve_indices(COLLISION_HEADER.copy())
    PartyRow.resolve_indices(PARTY_HEADER.copy())
    VictimRow.resolve_indices(VICTIM_HEADER.copy())
