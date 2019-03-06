#!/usr/bin/env python3

from switrs_to_sqlite.parsers import CollisionRow
import pytest

# A list of tuples, with each tuple containing a row ready to be parsed, and
# the answer that should be returned from doing so. The tuple is of the form
# (row, answer)
ROWS = (
    (
        # Case_ID                Collision_Year  Process_Date  Jurisdiction  Collision_Date  Collision_Time  Officer_ID  Reporting_District  DOW    CHP_Shift  Population  County_City_Location  Special_Condition  Beat_Type  CHP_Beat_Type      City_Division_LAPD  CHP_Beat_Class  Beat_Number  Primary_Road                       Secondary_Road   Distance      Direction  Intersection  Weather_1  Weather_2   State_Highway_Indicator  Caltrans_County  Caltrans_District  State_Route  Route_Suffix  Postmile_Prefix  Postmile       Location_Type    Ramp_Intersection  Side_Of_Highway  Tow_Away  Collision_Severity  Killed_Victims  Injured_Victims  Party_Count  Primary_Collision_Factor   PCF_Violation_Code  PCF_Violation_Category  PCF_Violation  PCF_Violation_Subsection  Hit_And_Run         Type_Of_Collision  Motor_Vehicle_Involved_With  Ped_Action                  Road_Surface  Road_Condition_1  Road_Condition_2  Lighting                    Control_Device  CHP_Road_Type  Pedestrian_Collision  Bicycle_Collision  Motorcycle_Collision  Truck_Collision  Not_Private_Property  Alcohol_Involved  Statewide_Vehicle_Type_At_Fault  CHP_Vehicle_Type_At_Fault  Severe_Injury_Count  Other_Visible_Injury_Count  Complaint_Of_Pain_Injury_Count  Pedestrian_Killed_Count  Pedestrian_Injured_Count  Bicyclist_Killed_Count  Bicyclist_Injured_Count  Motorcyclist_Killed_Count  Motorcyclist_Injured_Count  Primary_Ramp  Secondary_Ramp  Latitude    Longitude
        ['0100010101011401155',  '2001',         '20010416',   '0000',       '20010101',     '114',          '1155qq',   '0',                '1',   '4',       '4',        '198',                '-',               '0',       'A',               '',                 '0',            '073',       'DUBLIN_BL',                       'SCARLETT_CT',   '267000000',  'W',       'N',          'A',       'D',        'N',                     'abc',           '20',              '280',       'A',          'A',             '234000.222',  'H',             '8',               'N',             'Y',      '0',                '999',          '999',           '999',       'A',                       'C',                '01',                   '23152',       'A',                      'F',                'A',               'I',                         'A',                        'A',          'H',              'C',              'C',                        'D',            'A',           'N',                  'N',               'N',                  'N',             'NY',                 'N',              'B',                             '00',                      '0',                 '0',                        '0',                            '0',                     '0',                      '0',                    '0',                     '0',                       '0',                        'NF-NB',      'EF-EB',        '37.7749',  '122.4194'],
        ['0100010101011401155',                                0,                                            '1155qq',   '0',                       '4',       '4',        '198',                None,              '0',       'administrative',  None,               'not chp',      '073',       'DUBLIN_BL',                       'SCARLETT_CT',   267000000.,   'west',    False,        'clear',   'snowing',  False,                   'abc',           20,                280,         'A',          'A',             234000.222,    'highway',       8,                 'northbound',    True,     0,                  999,            999,             999,         'vehicle code violation',  'vehicle',          '01',                   23152,         'A',                      'felony',           'head-on',         'fixed object',              'no pedestrian involved',   'dry',        'normal',         'obstruction',    'dark with street lights',  'none',         'A',           False,                False,             False,                False,           False,                False,            'passenger car with trailer',    '00',                      0,                   0,                          0,                              0,                       0,                        0,                      0,                       0,                         0,                          'NF-NB',      'EF-EB',        37.7749,    -122.4194, "2001-01-01", "01:14:00", "2001-04-16"],
    ),
    (
        # Case_ID                Collision_Year  Process_Date  Jurisdiction  Collision_Date  Collision_Time  Officer_ID  Reporting_District  DOW    CHP_Shift  Population  County_City_Location  Special_Condition  Beat_Type  CHP_Beat_Type      City_Division_LAPD  CHP_Beat_Class  Beat_Number  Primary_Road                       Secondary_Road   Distance      Direction  Intersection  Weather_1  Weather_2   State_Highway_Indicator  Caltrans_County  Caltrans_District  State_Route  Route_Suffix  Postmile_Prefix  Postmile       Location_Type    Ramp_Intersection  Side_Of_Highway  Tow_Away  Collision_Severity  Killed_Victims  Injured_Victims  Party_Count  Primary_Collision_Factor   PCF_Violation_Code  PCF_Violation_Category  PCF_Violation  PCF_Violation_Subsection  Hit_And_Run         Type_Of_Collision  Motor_Vehicle_Involved_With  Ped_Action                  Road_Surface  Road_Condition_1  Road_Condition_2  Lighting                    Control_Device  CHP_Road_Type  Pedestrian_Collision  Bicycle_Collision  Motorcycle_Collision  Truck_Collision  Not_Private_Property  Alcohol_Involved  Statewide_Vehicle_Type_At_Fault  CHP_Vehicle_Type_At_Fault  Severe_Injury_Count  Other_Visible_Injury_Count  Complaint_Of_Pain_Injury_Count  Pedestrian_Killed_Count  Pedestrian_Injured_Count  Bicyclist_Killed_Count  Bicyclist_Injured_Count  Motorcyclist_Killed_Count  Motorcyclist_Injured_Count  Primary_Ramp  Secondary_Ramp  Latitude    Longitude
        ['3337743',              '2007',         '20080214',   '1900',       '20070821',     '0910',         '478242',   '0453',             '2',   '5',       '0',        '1949',               '0',               '8',       '0',               '-',                '-',            '43T1',      'HOXIE_AV',                        'IMPERIAL_HWY',  '400.02',     'S',       'Y',          '',        '-',        'Y',                     '123',           '99',              '80',        'B',          'B',             '38',          'I',             '4',               'E',             'N',      '4',                '0',            '0',             '1',         'E',                       'W',                '08',                   '22107',       '',                       'N',                'E',               'J',                         'E',                        'C',          'A',              '-',              'A',                        'A',            '4',           'Y',                  'Y',               'Y',                  'Y',             'Y',                  'Y',              'N',                             '99',                      '999',               '999',                      '999',                          '999',                   '999',                    '999',                  '999',                   '999',                     '999',                      'EF-EB',      '-',            '34.0522',  '118.2437'],
        ['3337743',                                            1900,                                         '478242',   '0453',                    '5',       '0',        '1949',               '0',               '8',       'not chp',         None,               None,           '43T1',      'HOXIE_AV',                        'IMPERIAL_HWY',  400.02,       'south',   True,         None,      None,       True,                    '123',           99,                80,          'B',          'B',             38,            'intersection',  4,                 'eastbound',     False,    4,                  0,              0,               1,           'fell asleep',             'welfare',                '08',                   22107,         None,                     'not hit and run',  'hit object',      'other object',              'in road',                  'snowy',      'holes',          None,             'daylight',                 'functioning',  '4',           True,                 True,              True,                 True,            True,                 True,             'pedestrian',                    None,                      999,                 999,                        999,                            999,                     999,                      999,                    999,                     999,                       999,                        'EF-EB',      None,           34.0522,    -118.2437, "2007-08-21", "09:10:00", "2008-02-14"],
    ),
    (
        # Case_ID                Collision_Year  Process_Date  Jurisdiction  Collision_Date  Collision_Time  Officer_ID  Reporting_District  DOW    CHP_Shift  Population  County_City_Location  Special_Condition  Beat_Type  CHP_Beat_Type      City_Division_LAPD  CHP_Beat_Class  Beat_Number  Primary_Road                       Secondary_Road   Distance      Direction  Intersection  Weather_1  Weather_2   State_Highway_Indicator  Caltrans_County  Caltrans_District  State_Route  Route_Suffix  Postmile_Prefix  Postmile       Location_Type    Ramp_Intersection  Side_Of_Highway  Tow_Away  Collision_Severity  Killed_Victims  Injured_Victims  Party_Count  Primary_Collision_Factor   PCF_Violation_Code  PCF_Violation_Category  PCF_Violation  PCF_Violation_Subsection  Hit_And_Run         Type_Of_Collision  Motor_Vehicle_Involved_With  Ped_Action                  Road_Surface  Road_Condition_1  Road_Condition_2  Lighting                    Control_Device  CHP_Road_Type  Pedestrian_Collision  Bicycle_Collision  Motorcycle_Collision  Truck_Collision  Not_Private_Property  Alcohol_Involved  Statewide_Vehicle_Type_At_Fault  CHP_Vehicle_Type_At_Fault  Severe_Injury_Count  Other_Visible_Injury_Count  Complaint_Of_Pain_Injury_Count  Pedestrian_Killed_Count  Pedestrian_Injured_Count  Bicyclist_Killed_Count  Bicyclist_Injured_Count  Motorcyclist_Killed_Count  Motorcyclist_Injured_Count  Primary_Ramp  Secondary_Ramp  Latitude    Longitude
        ['90180431',             '2015',         '20160516',   '9535',       '20151021',     '1635',         '021169',   '',                 '3',   '2',       '-',        '1948',               '3',               '-',       '-',               'A',                '2',            '-',         'I-710_(LONG_BEACH_FREEWAY)_N/B',  'FLORAL_DR',     '-',          '-',       '-',          'N',       'Y',        '-',                     '',              '',                '',          '',           '',              '',            '',              '',                '',              '',       '1',                '-',            '-',             '',          '-',                       '-',                '-',                    '-',           '-',                      'M',                '-',               '-',                         '-',                        '-',          '-',              'E',              '-',                        '-',            '',            '',                   '',                '',                   '',              '',                   '',               '-',                             '-',                       '-',                 '-',                        '-',                            '-',                     '-',                      '-',                    '-',                     '-',                       '-',                        '-',          '-',            '',         ''],
        ['90180431',                                           9535,                                         '021169',   None,                      '2',       None,       '1948',               '3',               None,      None,              'A',                'chp other',    None,        'I-710_(LONG_BEACH_FREEWAY)_N/B',  'FLORAL_DR',     None,         None,      None,         None,      None,       None,                    None,            None,              None,        None,         None,            None,          None,            None,              None,            None,     1,                  None,           None,            None,        None,                      None,               None,                   None,          None,                     'misdemeanor',      None,              None,                        None,                       None,         None,             'reduced width',  None,                       None,           None,          None,                 None,              None,                 None,            None,                 None,             None,                            None,                      None,                None,                       None,                           None,                    None,                     None,                   None,                    None,                      None,                       None,         None,           None,       None, "2015-10-21", "16:35:00", "2016-05-16"],
    ),
)


def test_collisionrows():
    for row, answer in ROWS:
        parsed_row = CollisionRow.parse_row(row)
        assert parsed_row == answer

def test_collisionrow_create_table():
    assert CollisionRow.create_table_statement() == (
        "CREATE TABLE "
        "Collision ("
        "Case_ID TEXT PRIMARY KEY, "
        "Jurisdiction INTEGER, "
        "Officer_ID TEXT, "
        "Reporting_District TEXT, "
        "CHP_Shift TEXT, "
        "Population TEXT, "
        "County_City_Location TEXT, "
        "Special_Condition TEXT, "
        "Beat_Type TEXT, "
        "CHP_Beat_Type TEXT, "
        "City_Division_LAPD TEXT, "
        "CHP_Beat_Class TEXT, "
        "Beat_Number TEXT, "
        "Primary_Road TEXT, "
        "Secondary_Road TEXT, "
        "Distance REAL, "
        "Direction TEXT, "
        "Intersection INTEGER, "
        "Weather_1 TEXT, "
        "Weather_2 TEXT, "
        "State_Highway_Indicator INTEGER, "
        "Caltrans_County TEXT, "
        "Caltrans_District INTEGER, "
        "State_Route INTEGER, "
        "Route_Suffix TEXT, "
        "Postmile_Prefix TEXT, "
        "Postmile REAL, "
        "Location_Type TEXT, "
        "Ramp_Intersection INTEGER, "
        "Side_Of_Highway TEXT, "
        "Tow_Away INTEGER, "
        "Collision_Severity INTEGER, "
        "Killed_Victims INTEGER, "
        "Injured_Victims INTEGER, "
        "Party_Count INTEGER, "
        "Primary_Collision_Factor TEXT, "
        "PCF_Violation_Code TEXT, "
        "PCF_Violation_Category TEXT, "
        "PCF_Violation INTEGER, "
        "PCF_Violation_Subsection TEXT, "
        "Hit_And_Run TEXT, "
        "Type_Of_Collision TEXT, "
        "Motor_Vehicle_Involved_With TEXT, "
        "Pedestrian_Action TEXT, "
        "Road_Surface TEXT, "
        "Road_Condition_1 TEXT, "
        "Road_Condition_2 TEXT, "
        "Lighting TEXT, "
        "Control_Device TEXT, "
        "CHP_Road_Type TEXT, "
        "Pedestrian_Collision INTEGER, "
        "Bicycle_Collision INTEGER, "
        "Motorcycle_Collision INTEGER, "
        "Truck_Collision INTEGER, "
        "Not_Private_Property INTEGER, "
        "Alcohol_Involved INTEGER, "
        "Statewide_Vehicle_Type_At_Fault TEXT, "
        "CHP_Vehicle_Type_At_Fault TEXT, "
        "Severe_Injury_Count INTEGER, "
        "Other_Visible_Injury_Count INTEGER, "
        "Complaint_Of_Pain_Injury_Count INTEGER, "
        "Pedestrian_Killed_Count INTEGER, "
        "Pedestrian_Injured_Count INTEGER, "
        "Bicyclist_Killed_Count INTEGER, "
        "Bicyclist_Injured_Count INTEGER, "
        "Motorcyclist_Killed_Count INTEGER, "
        "Motorcyclist_Injured_Count INTEGER, "
        "Primary_Ramp TEXT, "
        "Secondary_Ramp TEXT, "
        "Latitude REAL, "
        "Longitude REAL, "
        "Collision_Date TEXT, "
        "Collision_Time TEXT, "
        "Process_Date TEXT"
        ")"
    )

def test_partyrow_columns():
    assert CollisionRow.columns == [
        ("Case_ID", "TEXT", "PRIMARY KEY"),
        ("Jurisdiction", "INTEGER"),
        ("Officer_ID", "TEXT"),
        ("Reporting_District", "TEXT"),
        ("CHP_Shift", "TEXT"),
        ("Population", "TEXT"),
        ("County_City_Location", "TEXT"),
        ("Special_Condition", "TEXT"),
        ("Beat_Type", "TEXT"),
        ("CHP_Beat_Type", "TEXT"),
        ("City_Division_LAPD", "TEXT"),
        ("CHP_Beat_Class", "TEXT"),
        ("Beat_Number", "TEXT"),
        ("Primary_Road", "TEXT"),
        ("Secondary_Road", "TEXT"),
        ("Distance", "REAL"),
        ("Direction", "TEXT"),
        ("Intersection", "INTEGER"),
        ("Weather_1", "TEXT"),
        ("Weather_2", "TEXT"),
        ("State_Highway_Indicator", "INTEGER"),
        ("Caltrans_County", "TEXT"),
        ("Caltrans_District", "INTEGER"),
        ("State_Route", "INTEGER"),
        ("Route_Suffix", "TEXT"),
        ("Postmile_Prefix", "TEXT"),
        ("Postmile", "REAL"),
        ("Location_Type", "TEXT"),
        ("Ramp_Intersection", "INTEGER"),
        ("Side_Of_Highway", "TEXT"),
        ("Tow_Away", "INTEGER"),
        ("Collision_Severity", "INTEGER"),
        ("Killed_Victims", "INTEGER"),
        ("Injured_Victims", "INTEGER"),
        ("Party_Count", "INTEGER"),
        ("Primary_Collision_Factor", "TEXT"),
        ("PCF_Violation_Code", "TEXT"),
        ("PCF_Violation_Category", "TEXT"),
        ("PCF_Violation", "INTEGER"),
        ("PCF_Violation_Subsection", "TEXT"),
        ("Hit_And_Run", "TEXT"),
        ("Type_Of_Collision", "TEXT"),
        ("Motor_Vehicle_Involved_With", "TEXT"),
        ("Pedestrian_Action", "TEXT"),
        ("Road_Surface", "TEXT"),
        ("Road_Condition_1", "TEXT"),
        ("Road_Condition_2", "TEXT"),
        ("Lighting", "TEXT"),
        ("Control_Device", "TEXT"),
        ("CHP_Road_Type", "TEXT"),
        ("Pedestrian_Collision", "INTEGER"),
        ("Bicycle_Collision", "INTEGER"),
        ("Motorcycle_Collision", "INTEGER"),
        ("Truck_Collision", "INTEGER"),
        ("Not_Private_Property", "INTEGER"),
        ("Alcohol_Involved", "INTEGER"),
        ("Statewide_Vehicle_Type_At_Fault", "TEXT"),
        ("CHP_Vehicle_Type_At_Fault", "TEXT"),
        ("Severe_Injury_Count", "INTEGER"),
        ("Other_Visible_Injury_Count", "INTEGER"),
        ("Complaint_Of_Pain_Injury_Count", "INTEGER"),
        ("Pedestrian_Killed_Count", "INTEGER"),
        ("Pedestrian_Injured_Count", "INTEGER"),
        ("Bicyclist_Killed_Count", "INTEGER"),
        ("Bicyclist_Injured_Count", "INTEGER"),
        ("Motorcyclist_Killed_Count", "INTEGER"),
        ("Motorcyclist_Injured_Count", "INTEGER"),
        ("Primary_Ramp", "TEXT"),
        ("Secondary_Ramp", "TEXT"),
        ("Latitude", "REAL"),
        ("Longitude", "REAL"),
        ("Collision_Date", "TEXT"),
        ("Collision_Time", "TEXT"),
        ("Process_Date", "TEXT"),
    ]
