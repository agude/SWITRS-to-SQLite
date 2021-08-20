#!/usr/bin/env python3

from switrs_to_sqlite.parsers import CollisionRow


# A list of tuples, with each tuple containing a row ready to be parsed, and
# the answer that should be returned from doing so. The tuple is of the form
# (row, answer)
ROWS = (
    (
        # Case_ID                Collision_Year  Process_Date  Jurisdiction  Collision_Date  Collision_Time  Officer_ID  Reporting_District  DOW    CHP_Shift  Population  County_City_Location County_Location Special_Condition  Beat_Type  CHP_Beat_Type      City_Division_LAPD  CHP_Beat_Class  Beat_Number  Primary_Road                       Secondary_Road   Distance      Direction  Intersection  Weather_1  Weather_2   State_Highway_Indicator  Caltrans_County  Caltrans_District  State_Route  Route_Suffix  Postmile_Prefix  Postmile       Location_Type    Ramp_Intersection  Side_Of_Highway  Tow_Away  Collision_Severity       Killed_Victims  Injured_Victims  Party_Count  Primary_Collision_Factor   PCF_Violation_Code  PCF_Violation_Category  PCF_Violation  PCF_Violation_Subsection  Hit_And_Run         Type_Of_Collision  Motor_Vehicle_Involved_With  Ped_Action                  Road_Surface  Road_Condition_1  Road_Condition_2  Lighting                    Control_Device  CHP_Road_Type  Pedestrian_Collision  Bicycle_Collision  Motorcycle_Collision  Truck_Collision  Not_Private_Property  Alcohol_Involved  Statewide_Vehicle_Type_At_Fault  CHP_Vehicle_Type_At_Fault  Severe_Injury_Count  Other_Visible_Injury_Count  Complaint_Of_Pain_Injury_Count  Pedestrian_Killed_Count  Pedestrian_Injured_Count  Bicyclist_Killed_Count  Bicyclist_Injured_Count  Motorcyclist_Killed_Count  Motorcyclist_Injured_Count  Primary_Ramp  Secondary_Ramp  Latitude    Longitude
        ['0100010101011401155',  '2001',         '20010416',   '0000',       '20010101',     '114',          '1155qq',   '0',                '1',   '4',       '4',        '0198',                              '-',               '0',       'A',               '',                 '0',            '073',       'DUBLIN_BL',                       'SCARLETT_CT',   '267000000',  'W',       'N',          'A',       'D',        'N',                     'abc',           '20',              '280',       'A',          'A',             '234000.222',  'H',             '8',               'N',             'Y',      '0',                     '999',          '999',           '999',       'A',                       'C',                '01',                   '23152',       'A',                      'F',                'A',               'I',                         'A',                        'A',          'H',              'C',              'C',                        'D',            'A',           'N',                  'N',               'N',                  'N',             'NY',                 'N',              'B',                             '00',                      '0',                 '0',                        '0',                            '0',                     '0',                      '0',                    '0',                     '0',                       '0',                        'NF-NB',      'EF-EB',        '37.7749',  '122.4194'],
        ['0100010101011401155',                                0,                                            '1155qq',   '0',                       '4',       '4',        '0198',              'alameda',      None,              '0',       'administrative',  None,               'not chp',      '073',       'DUBLIN_BL',                       'SCARLETT_CT',   267000000.,   'west',    False,        'clear',   'snowing',  False,                   'abc',           20,                280,         'A',          'A',             234000.222,    'highway',       8,                 'northbound',    True,     'property damage only',  999,            999,             999,         'vehicle code violation',  'vehicle',          'dui',                  23152,         'A',                      'felony',           'head-on',         'fixed object',              'no pedestrian involved',   'dry',        'normal',         'obstruction',    'dark with street lights',  'none',         'A',           False,                False,             False,                False,           False,                False,            'passenger car with trailer',    '00',                      0,                   0,                          0,                              0,                       0,                        0,                      0,                       0,                         0,                          'NF-NB',      'EF-EB',        37.7749,    -122.4194, "2001-01-01", "01:14:00", "2001-04-16"],
    ),
    (
        # Case_ID                Collision_Year  Process_Date  Jurisdiction  Collision_Date  Collision_Time  Officer_ID  Reporting_District  DOW    CHP_Shift  Population  County_City_Location County_Location Special_Condition  Beat_Type  CHP_Beat_Type      City_Division_LAPD  CHP_Beat_Class  Beat_Number  Primary_Road                       Secondary_Road   Distance      Direction  Intersection  Weather_1  Weather_2   State_Highway_Indicator  Caltrans_County  Caltrans_District  State_Route  Route_Suffix  Postmile_Prefix  Postmile       Location_Type    Ramp_Intersection  Side_Of_Highway  Tow_Away  Collision_Severity       Killed_Victims  Injured_Victims  Party_Count  Primary_Collision_Factor   PCF_Violation_Code  PCF_Violation_Category  PCF_Violation  PCF_Violation_Subsection  Hit_And_Run         Type_Of_Collision  Motor_Vehicle_Involved_With  Ped_Action                  Road_Surface  Road_Condition_1  Road_Condition_2  Lighting                    Control_Device  CHP_Road_Type  Pedestrian_Collision  Bicycle_Collision  Motorcycle_Collision  Truck_Collision  Not_Private_Property  Alcohol_Involved  Statewide_Vehicle_Type_At_Fault  CHP_Vehicle_Type_At_Fault  Severe_Injury_Count  Other_Visible_Injury_Count  Complaint_Of_Pain_Injury_Count  Pedestrian_Killed_Count  Pedestrian_Injured_Count  Bicyclist_Killed_Count  Bicyclist_Injured_Count  Motorcyclist_Killed_Count  Motorcyclist_Injured_Count  Primary_Ramp  Secondary_Ramp  Latitude    Longitude
        ['3337743',              '2007',         '20080214',   '1900',       '20070821',     '0910',         '478242',   '0453',             '2',   '5',       '0',        '1949',                              '0',               '8',       '0',               '-',                '-',            '43T1',      'HOXIE_AV',                        'IMPERIAL_HWY',  '400.02',     'S',       'Y',          '',        '-',        'Y',                     '123',           '99',              '80',        'B',          'B',             '38',          'I',             '4',               'E',             'N',      '4',                     '0',            '0',             '1',         'E',                       'W',                '08',                   '22107',       '',                       'N',                'E',               'J',                         'E',                        'C',          'A',              '-',              'A',                        'A',            '4',           'Y',                  'Y',               'Y',                  'Y',             'Y',                  'Y',              'N',                             '99',                      '999',               '999',                      '999',                          '999',                   '999',                    '999',                  '999',                   '999',                     '999',                      'EF-EB',      '-',            '34.0522',  '118.2437'],
        ['3337743',                                            1900,                                         '478242',   '0453',                    '5',       '0',        '1949',              'los angeles',  '0',               '8',       'not chp',         None,               None,           '43T1',      'HOXIE_AV',                        'IMPERIAL_HWY',  400.02,       'south',   True,         None,      None,       True,                    '123',           99,                80,          'B',          'B',             38,            'intersection',  4,                 'eastbound',     False,    'pain',                  0,              0,               1,           'fell asleep',             'welfare',          'improper turning',     22107,         None,                     'not hit and run',  'hit object',      'other object',              'in road',                  'snowy',      'holes',          None,             'daylight',                 'functioning',  '4',           True,                 True,              True,                 True,            True,                 True,             'pedestrian',                    None,                      999,                 999,                        999,                            999,                     999,                      999,                    999,                     999,                       999,                        'EF-EB',      None,           34.0522,    -118.2437, "2007-08-21", "09:10:00", "2008-02-14"],
    ),
    (
        # Case_ID                Collision_Year  Process_Date  Jurisdiction  Collision_Date  Collision_Time  Officer_ID  Reporting_District  DOW    CHP_Shift  Population  County_City_Location County_Location Special_Condition  Beat_Type  CHP_Beat_Type      City_Division_LAPD  CHP_Beat_Class  Beat_Number  Primary_Road                       Secondary_Road   Distance      Direction  Intersection  Weather_1  Weather_2   State_Highway_Indicator  Caltrans_County  Caltrans_District  State_Route  Route_Suffix  Postmile_Prefix  Postmile       Location_Type    Ramp_Intersection  Side_Of_Highway  Tow_Away  Collision_Severity       Killed_Victims  Injured_Victims  Party_Count  Primary_Collision_Factor   PCF_Violation_Code  PCF_Violation_Category  PCF_Violation  PCF_Violation_Subsection  Hit_And_Run         Type_Of_Collision  Motor_Vehicle_Involved_With  Ped_Action                  Road_Surface  Road_Condition_1  Road_Condition_2  Lighting                    Control_Device  CHP_Road_Type  Pedestrian_Collision  Bicycle_Collision  Motorcycle_Collision  Truck_Collision  Not_Private_Property  Alcohol_Involved  Statewide_Vehicle_Type_At_Fault  CHP_Vehicle_Type_At_Fault  Severe_Injury_Count  Other_Visible_Injury_Count  Complaint_Of_Pain_Injury_Count  Pedestrian_Killed_Count  Pedestrian_Injured_Count  Bicyclist_Killed_Count  Bicyclist_Injured_Count  Motorcyclist_Killed_Count  Motorcyclist_Injured_Count  Primary_Ramp  Secondary_Ramp  Latitude    Longitude
        ['90180431',             '2015',         '20160516',   '9535',       '20151021',     '1635',         '021169',   '',                 '3',   '2',       '-',        '',                                  '3',               '-',       '-',               'A',                '2',            '-',         'I-710_(LONG_BEACH_FREEWAY)_N/B',  'FLORAL_DR',     '-',          '-',       '-',          'N',       'Y',        '-',                     '',              '',                '',          '',           '',              '',            '',              '',                '',              '',       '1',                     '-',            '-',             '',          '-',                       '-',                '-',                    '-',           '-',                      'M',                '-',               '-',                         '-',                        '-',          '-',              'E',              '-',                        '-',            '',            '',                   '',                '',                   '',              '',                   '',               '-',                             '-',                       '-',                 '-',                        '-',                            '-',                     '-',                      '-',                    '-',                     '-',                       '-',                        '-',          '-',            '',         ''],
        ['90180431',                                           9535,                                         '021169',   None,                      '2',       None,       None,                None,           '3',               None,      None,              'A',                'chp other',    None,        'I-710_(LONG_BEACH_FREEWAY)_N/B',  'FLORAL_DR',     None,         None,      None,         None,      None,       None,                    None,            None,              None,        None,         None,            None,          None,            None,              None,            None,     'fatal',                 None,           None,            None,        None,                      None,               None,                   None,          None,                     'misdemeanor',      None,              None,                        None,                       None,         None,             'reduced width',  None,                       None,           None,          None,                 None,              None,                 None,            None,                 None,             None,                            None,                      None,                None,                       None,                           None,                    None,                     None,                   None,                    None,                      None,                       None,         None,           None,       None, "2015-10-21", "16:35:00", "2016-05-16"],
    ),
)


def test_collisionrows():
    for row, answer in ROWS:
        parsed_row = CollisionRow.parse_row(row)
        assert parsed_row == answer

def test_collisionrow_create_table():
    assert CollisionRow.create_table_statement() == (
        "CREATE TABLE "
        "collisions ("
        "case_id TEXT PRIMARY KEY, "
        "jurisdiction INTEGER, "
        "officer_id TEXT, "
        "reporting_district TEXT, "
        "chp_shift TEXT, "
        "population TEXT, "
        "county_city_location TEXT, "
        "county_location TEXT, "
        "special_condition TEXT, "
        "beat_type TEXT, "
        "chp_beat_type TEXT, "
        "city_division_lapd TEXT, "
        "chp_beat_class TEXT, "
        "beat_number TEXT, "
        "primary_road TEXT, "
        "secondary_road TEXT, "
        "distance REAL, "
        "direction TEXT, "
        "intersection INTEGER, "
        "weather_1 TEXT, "
        "weather_2 TEXT, "
        "state_highway_indicator INTEGER, "
        "caltrans_county TEXT, "
        "caltrans_district INTEGER, "
        "state_route INTEGER, "
        "route_suffix TEXT, "
        "postmile_prefix TEXT, "
        "postmile REAL, "
        "location_type TEXT, "
        "ramp_intersection INTEGER, "
        "side_of_highway TEXT, "
        "tow_away INTEGER, "
        "collision_severity TEXT, "
        "killed_victims INTEGER, "
        "injured_victims INTEGER, "
        "party_count INTEGER, "
        "primary_collision_factor TEXT, "
        "pcf_violation_code TEXT, "
        "pcf_violation_category TEXT, "
        "pcf_violation INTEGER, "
        "pcf_violation_subsection TEXT, "
        "hit_and_run TEXT, "
        "type_of_collision TEXT, "
        "motor_vehicle_involved_with TEXT, "
        "pedestrian_action TEXT, "
        "road_surface TEXT, "
        "road_condition_1 TEXT, "
        "road_condition_2 TEXT, "
        "lighting TEXT, "
        "control_device TEXT, "
        "chp_road_type TEXT, "
        "pedestrian_collision INTEGER, "
        "bicycle_collision INTEGER, "
        "motorcycle_collision INTEGER, "
        "truck_collision INTEGER, "
        "not_private_property INTEGER, "
        "alcohol_involved INTEGER, "
        "statewide_vehicle_type_at_fault TEXT, "
        "chp_vehicle_type_at_fault TEXT, "
        "severe_injury_count INTEGER, "
        "other_visible_injury_count INTEGER, "
        "complaint_of_pain_injury_count INTEGER, "
        "pedestrian_killed_count INTEGER, "
        "pedestrian_injured_count INTEGER, "
        "bicyclist_killed_count INTEGER, "
        "bicyclist_injured_count INTEGER, "
        "motorcyclist_killed_count INTEGER, "
        "motorcyclist_injured_count INTEGER, "
        "primary_ramp TEXT, "
        "secondary_ramp TEXT, "
        "latitude REAL, "
        "longitude REAL, "
        "collision_date TEXT, "
        "collision_time TEXT, "
        "process_date TEXT"
        ")"
    )

def test_partyrow_columns():
    assert CollisionRow.columns == [
        ("case_id", "TEXT", "PRIMARY KEY"),
        ("jurisdiction", "INTEGER"),
        ("officer_id", "TEXT"),
        ("reporting_district", "TEXT"),
        ("chp_shift", "TEXT"),
        ("population", "TEXT"),
        ("county_city_location", "TEXT"),
        ("county_location", "TEXT"),
        ("special_condition", "TEXT"),
        ("beat_type", "TEXT"),
        ("chp_beat_type", "TEXT"),
        ("city_division_lapd", "TEXT"),
        ("chp_beat_class", "TEXT"),
        ("beat_number", "TEXT"),
        ("primary_road", "TEXT"),
        ("secondary_road", "TEXT"),
        ("distance", "REAL"),
        ("direction", "TEXT"),
        ("intersection", "INTEGER"),
        ("weather_1", "TEXT"),
        ("weather_2", "TEXT"),
        ("state_highway_indicator", "INTEGER"),
        ("caltrans_county", "TEXT"),
        ("caltrans_district", "INTEGER"),
        ("state_route", "INTEGER"),
        ("route_suffix", "TEXT"),
        ("postmile_prefix", "TEXT"),
        ("postmile", "REAL"),
        ("location_type", "TEXT"),
        ("ramp_intersection", "INTEGER"),
        ("side_of_highway", "TEXT"),
        ("tow_away", "INTEGER"),
        ("collision_severity", "TEXT"),
        ("killed_victims", "INTEGER"),
        ("injured_victims", "INTEGER"),
        ("party_count", "INTEGER"),
        ("primary_collision_factor", "TEXT"),
        ("pcf_violation_code", "TEXT"),
        ("pcf_violation_category", "TEXT"),
        ("pcf_violation", "INTEGER"),
        ("pcf_violation_subsection", "TEXT"),
        ("hit_and_run", "TEXT"),
        ("type_of_collision", "TEXT"),
        ("motor_vehicle_involved_with", "TEXT"),
        ("pedestrian_action", "TEXT"),
        ("road_surface", "TEXT"),
        ("road_condition_1", "TEXT"),
        ("road_condition_2", "TEXT"),
        ("lighting", "TEXT"),
        ("control_device", "TEXT"),
        ("chp_road_type", "TEXT"),
        ("pedestrian_collision", "INTEGER"),
        ("bicycle_collision", "INTEGER"),
        ("motorcycle_collision", "INTEGER"),
        ("truck_collision", "INTEGER"),
        ("not_private_property", "INTEGER"),
        ("alcohol_involved", "INTEGER"),
        ("statewide_vehicle_type_at_fault", "TEXT"),
        ("chp_vehicle_type_at_fault", "TEXT"),
        ("severe_injury_count", "INTEGER"),
        ("other_visible_injury_count", "INTEGER"),
        ("complaint_of_pain_injury_count", "INTEGER"),
        ("pedestrian_killed_count", "INTEGER"),
        ("pedestrian_injured_count", "INTEGER"),
        ("bicyclist_killed_count", "INTEGER"),
        ("bicyclist_injured_count", "INTEGER"),
        ("motorcyclist_killed_count", "INTEGER"),
        ("motorcyclist_injured_count", "INTEGER"),
        ("primary_ramp", "TEXT"),
        ("secondary_ramp", "TEXT"),
        ("latitude", "REAL"),
        ("longitude", "REAL"),
        ("collision_date", "TEXT"),
        ("collision_time", "TEXT"),
        ("process_date", "TEXT"),
    ]
