from switrs_to_sqlite.converters import convert, negative, string_to_bool, county_city_location_to_county, cellphone_use_to_bool, non_standard_str_to_bool
from switrs_to_sqlite.datatypes import DataType
import switrs_to_sqlite.make_map as mm
import switrs_to_sqlite.value_maps as vm


DEFAULT_NULLS = ["", "-"]

COLLISION_ROW = (
    (0, "case_id", DataType.TEXT, None, convert, None),
    (3, "jurisdiction", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (6, "officer_id", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (7, "reporting_district", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (9, "chp_shift", DataType.TEXT, DEFAULT_NULLS, convert, vm.CHP_SHIFT),
    (10, "population", DataType.TEXT, DEFAULT_NULLS, convert, vm.POPULATION),
    (11, "county_city_location", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (11, "county_location", DataType.TEXT, DEFAULT_NULLS, county_city_location_to_county, vm.COUNTIES),
    (12, "special_condition", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (13, "beat_type", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (14, "chp_beat_type", DataType.TEXT, DEFAULT_NULLS, convert, vm.CHP_BEAT_TYPE),
    (15, "city_division_lapd", DataType.TEXT, DEFAULT_NULLS + ["0"], convert, None),
    (16, "chp_beat_class", DataType.TEXT, DEFAULT_NULLS, convert, vm.CHP_BEAT_CLASS),
    (17, "beat_number", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (18, "primary_road", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (19, "secondary_road", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (20, "distance", DataType.REAL, DEFAULT_NULLS, convert, None),
    (21, "direction", DataType.TEXT, DEFAULT_NULLS, convert, vm.DIRECTION),
    (22, "intersection", DataType.INTEGER, DEFAULT_NULLS, string_to_bool, None),
    (23, "weather_1", DataType.TEXT, DEFAULT_NULLS + ['N', 'Y'], convert, vm.WEATHER),
    (24, "weather_2", DataType.TEXT, DEFAULT_NULLS + ['N', 'Y'], convert, vm.WEATHER),
    (25, "state_highway_indicator", DataType.INTEGER, DEFAULT_NULLS, string_to_bool, None),
    (26, "caltrans_county", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (27, "caltrans_district", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (28, "state_route", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (29, "route_suffix", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (30, "postmile_prefix", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (31, "postmile", DataType.REAL, DEFAULT_NULLS, convert, None),
    (32, "location_type", DataType.TEXT, DEFAULT_NULLS, convert, vm.LOCATION_TYPE),
    (33, "ramp_intersection", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (34, "side_of_highway", DataType.TEXT, DEFAULT_NULLS, convert, vm.SIDE_OF_HIGHWAY),
    (35, "tow_away", DataType.INTEGER, DEFAULT_NULLS, string_to_bool, None),
    (36, "collision_severity", DataType.TEXT, DEFAULT_NULLS, convert, vm.COLLISION_SEVERITY),
    (37, "killed_victims", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (38, "injured_victims", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (39, "party_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (40, "primary_collision_factor", DataType.TEXT, DEFAULT_NULLS, convert, vm.PRIMARY_COLLISION_FACTOR),
    (41, "pcf_violation_code", DataType.TEXT, DEFAULT_NULLS, convert, vm.PCF_VIOLATION_CODE),
    (42, "pcf_violation_category", DataType.TEXT, DEFAULT_NULLS, convert, vm.PCF_VIOLATION_CATEGORY),
    (43, "pcf_violation", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (44, "pcf_violation_subsection", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (45, "hit_and_run", DataType.TEXT, DEFAULT_NULLS, convert, vm.HIT_AND_RUN),
    (46, "type_of_collision", DataType.TEXT, DEFAULT_NULLS + ["M"], convert, vm.COLLISION_TYPE),
    (47, "motor_vehicle_involved_with", DataType.TEXT, DEFAULT_NULLS, convert, vm.INVOLVED_WITH),
    (48, "pedestrian_action", DataType.TEXT, DEFAULT_NULLS, convert, vm.PEDESTRIAN_ACTION),
    (49, "road_surface", DataType.TEXT, DEFAULT_NULLS, convert, vm.ROAD_SURFACE),
    (50, "road_condition_1", DataType.TEXT, DEFAULT_NULLS, convert, vm.ROAD_CONDITION),
    (51, "road_condition_2", DataType.TEXT, DEFAULT_NULLS, convert, vm.ROAD_CONDITION),
    (52, "lighting", DataType.TEXT, DEFAULT_NULLS, convert, vm.LIGHTING),
    (53, "control_device", DataType.TEXT, DEFAULT_NULLS, convert, vm.CONTROL_DEVICE),
    (54, "chp_road_type", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (55, "pedestrian_collision", DataType.INTEGER, None, string_to_bool, None),
    (56, "bicycle_collision", DataType.INTEGER, None, string_to_bool, None),
    (57, "motorcycle_collision", DataType.INTEGER, None, string_to_bool, None),
    (58, "truck_collision", DataType.INTEGER, None, string_to_bool, None),
    (59, "not_private_property", DataType.INTEGER, DEFAULT_NULLS, string_to_bool, None),
    (60, "alcohol_involved", DataType.INTEGER, DEFAULT_NULLS, string_to_bool, None),
    (61, "statewide_vehicle_type_at_fault", DataType.TEXT, DEFAULT_NULLS, convert, vm.STATEWIDE_VEHICLE_TYPE),
    (62, "chp_vehicle_type_at_fault", DataType.TEXT, DEFAULT_NULLS, convert, vm.CHP_VEHICLE_TYPE),
    (63, "severe_injury_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (64, "other_visible_injury_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (65, "complaint_of_pain_injury_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (66, "pedestrian_killed_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (67, "pedestrian_injured_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (68, "bicyclist_killed_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (69, "bicyclist_injured_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (70, "motorcyclist_killed_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (71, "motorcyclist_injured_count", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (72, "primary_ramp", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (73, "secondary_ramp", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (74, "latitude", DataType.REAL, DEFAULT_NULLS, convert, None),
    (75, "longitude", DataType.REAL, DEFAULT_NULLS, negative, None),
)

COLLISION_DATE_TABLE = (
    (4, "collision_date", DataType.TEXT),
    (5, "collision_time", DataType.TEXT),
    (2, "process_date", DataType.TEXT),
)

PARTY_ROW = (
    (0, "case_id", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (1, "party_number", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (2, "party_type", DataType.TEXT, DEFAULT_NULLS, convert, vm.PARTY_TYPE),
    (3, "at_fault", DataType.INTEGER, DEFAULT_NULLS, string_to_bool, None),
    (4, "party_sex", DataType.TEXT, DEFAULT_NULLS, convert, vm.SEX),
    (5, "party_age", DataType.INTEGER, DEFAULT_NULLS + ["998"], convert, None),
    (6, "party_sobriety", DataType.TEXT, DEFAULT_NULLS, convert, vm.SOBRIETY),
    (7, "party_drug_physical", DataType.TEXT, DEFAULT_NULLS, convert, vm.DRUG),
    (8, "direction_of_travel", DataType.TEXT, DEFAULT_NULLS, convert, vm.DIRECTION),
    (9, "party_safety_equipment_1", DataType.TEXT, DEFAULT_NULLS, convert, vm.SAFETY),
    (10, "party_safety_equipment_2", DataType.TEXT, DEFAULT_NULLS, convert, vm.SAFETY),
    (11, "financial_responsibility", DataType.TEXT, DEFAULT_NULLS, convert, vm.FINANCIAL),
    (12, "hazardous_materials", DataType.INTEGER, DEFAULT_NULLS, non_standard_str_to_bool, None),
    (13, "cellphone_in_use", DataType.INTEGER, DEFAULT_NULLS, cellphone_use_to_bool, None),
    (13, "cellphone_use_type", DataType.TEXT, DEFAULT_NULLS, convert, vm.CELLPHONE_USE_TYPE),
    (14, "school_bus_related", DataType.INTEGER, DEFAULT_NULLS, non_standard_str_to_bool, None),
    (15, "oaf_violation_code", DataType.TEXT, DEFAULT_NULLS, convert, vm.OAF_VIOLATION_CODE),
    (16, "oaf_violation_category", DataType.TEXT, DEFAULT_NULLS + ["00"], convert, vm.OAF_VIOLATION_CATEGORY),
    (17, "oaf_violation_section", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (18, "oaf_violation_suffix", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (19, "other_associate_factor_1", DataType.TEXT, DEFAULT_NULLS, convert, vm.OTHER_FACTOR),
    (20, "other_associate_factor_2", DataType.TEXT, DEFAULT_NULLS, convert, vm.OTHER_FACTOR),
    (21, "party_number_killed", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (22, "party_number_injured", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (23, "movement_preceding_collision", DataType.TEXT, DEFAULT_NULLS, convert, vm.MOVEMENT_PRECEDING),
    (24, "vehicle_year", DataType.INTEGER, DEFAULT_NULLS + ["9999"], convert, None),
    (25, "vehicle_make", DataType.TEXT, DEFAULT_NULLS, convert, mm.MAKE_MAP),
    (26, "statewide_vehicle_type", DataType.TEXT, DEFAULT_NULLS, convert, vm.STATEWIDE_VEHICLE_TYPE),
    (27, "chp_vehicle_type_towing", DataType.TEXT, DEFAULT_NULLS, convert, vm.CHP_VEHICLE_TYPE),
    (28, "chp_vehicle_type_towed", DataType.TEXT, DEFAULT_NULLS, convert, vm.CHP_VEHICLE_TYPE),
    (29, "party_race", DataType.TEXT, DEFAULT_NULLS, convert, vm.RACE),
)

VICTIM_ROW = (
    (0, "case_id", DataType.TEXT, DEFAULT_NULLS, convert, None),
    (1, "party_number", DataType.INTEGER, DEFAULT_NULLS, convert, None),
    (2, "victim_role", DataType.TEXT, DEFAULT_NULLS, convert, vm.ROLE),
    (3, "victim_sex", DataType.TEXT, DEFAULT_NULLS, convert, vm.SEX),
    (4, "victim_age", DataType.INTEGER, DEFAULT_NULLS + ["998"], convert, None),
    (5, "victim_degree_of_injury", DataType.TEXT, DEFAULT_NULLS, convert, vm.DEGREE_OF_INJURY),
    (6, "victim_seating_position", DataType.TEXT, DEFAULT_NULLS, convert, vm.SEATING_POSITION),
    (7, "victim_safety_equipment_1", DataType.TEXT, DEFAULT_NULLS, convert, vm.SAFETY),
    (8, "victim_safety_equipment_2", DataType.TEXT, DEFAULT_NULLS, convert, vm.SAFETY),
    (9, "victim_ejected", DataType.TEXT, DEFAULT_NULLS, convert, vm.EJECTED),
)
