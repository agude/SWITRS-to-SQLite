#!/usr/bin/env python3

from switrs_to_sqlite.parsers import PartyRow


# A list of tuples, with each tuple containing a row ready to be parsed, and
# the answer that should be returned from doing so. The tuple is of the form
# (row, answer)
ROWS = (
    (
        #      Case_ID     Party_Number  Party_Type    At_Fault  Party_Sex  Party_Age  Party_Sobriety  Party_Drug_Physical  Direction_Of_Travel  Party_Safety_Equipment_1  Party_Safety_Equipment_2  Financial_Responsibility  Hazardous_Materials  Cellphone_Use  School_Bus_Related  OAF_Violation_Code  OAF_Violation_Category  OAF_Violation_Section  OAF_Violation_Suffix  Other_Associate_Factor_1  Other_Associate_Factor_2  Party_Number_Killed  Party_Number_Injured  Movement_Preceding_Collision  Vehicle_Year  Vehicle_Make  Statewide_Vehicle_Type  CHP_Vehicle_Type_Towing  CHP_Vehicle_Type_Towed  Party_Race
        [      '097293',   '1',          '1',          'Y',      'M',       '20',      'A',            'H',                 'E',                 'A',                      'F',                      'N',                      'A',                 'D',           'E',                'C',                '18',                   '12345',               'A',                  'N',                      'A',                      '0',                 '0',                  'M',                          '1996',       'FORD',       'A',                    '08',                    '00',                   'W'],
        [None, '097293',   1,            'driver',     True,     'male',    20,        'A',            'H',                 'E',                 'A',                      'F',                      'N',                      'A',                 'D',           'E',                'C',                '18',                   12345,                 'A',                  'N',                      'A',                      0,                   0,                    'other unsafe turning',       1996,         'ford',       'passenger car',        '08',                    '00',                   'white',],
    ),
    (
        #      Case_ID     Party_Number  Party_Type    At_Fault  Party_Sex  Party_Age  Party_Sobriety  Party_Drug_Physical  Direction_Of_Travel  Party_Safety_Equipment_1  Party_Safety_Equipment_2  Financial_Responsibility  Hazardous_Materials  Cellphone_Use  School_Bus_Related  OAF_Violation_Code  OAF_Violation_Category  OAF_Violation_Section  OAF_Violation_Suffix  Other_Associate_Factor_1  Other_Associate_Factor_2  Party_Number_Killed  Party_Number_Injured  Movement_Preceding_Collision  Vehicle_Year  Vehicle_Make  Statewide_Vehicle_Type  CHP_Vehicle_Type_Towing  CHP_Vehicle_Type_Towed  Party_Race
        [      '0018200',  '3',          '4',          'N',      'F',       '999',     'H',            'E',                 'N',                 'G',                      '-',                      'Y',                      '-',                 'B',           '-',                'W',                '29',                   '',                    'B',                  'G',                      '-',                      '1',                 '1',                  'A',                          '1987',       'BMW',        'O',                    '97',                    '98',                   'H'],
        [None, '0018200',  3,            'bicyclist',  False,    'female',  999,       'H',            'E',                 'N',                 'G',                      None,                     'Y',                      None,                'B',           None,               'W',                '29',                   None,                  'B',                  'G',                      None,                     1,                   1,                    'stopped',                    1987,         'bmw',        'moped',                '97',                    '98',                   'hispanic',],
    ),
    (
        #      Case_ID     Party_Number  Party_Type    At_Fault  Party_Sex  Party_Age  Party_Sobriety  Party_Drug_Physical  Direction_Of_Travel  Party_Safety_Equipment_1  Party_Safety_Equipment_2  Financial_Responsibility  Hazardous_Materials  Cellphone_Use  School_Bus_Related  OAF_Violation_Code  OAF_Violation_Category  OAF_Violation_Section  OAF_Violation_Suffix  Other_Associate_Factor_1  Other_Associate_Factor_2  Party_Number_Killed  Party_Number_Injured  Movement_Preceding_Collision  Vehicle_Year  Vehicle_Make  Statewide_Vehicle_Type  CHP_Vehicle_Type_Towing  CHP_Vehicle_Type_Towed  Party_Race
        [      '0036598',  '2',          '-',          '-',      '-',       '998',     '-',            '-',                 '-',                 '-',                      '-',                      '',                       '-',                 '-',           '-',                '-',                '00',                   '',                    '',                   '-',                      '-',                      '20',                '2',                  '-',                          '9999',       'NOT_MAP',    '-',                    '99',                    '99',                   ''],
        [None, '0036598',  2,            None,         None,     None,      None,      None,           None,                None,                None,                     None,                     None,                     None,                None,          None,               None,               None,                   None,                  None,                 None,                     None,                     20,                  2,                    None,                         None,         'NOT_MAP',    None,                   None,                    None,                   None],
    ),
)


def test_partyrows():
    for row, answer in ROWS:
        parsed_row = PartyRow.parse_row(row)
        assert parsed_row == answer

def test_partyrow_create_table():
    assert PartyRow.create_table_statement() == (
        "CREATE TABLE "
        "parties ("
        "id INTEGER PRIMARY KEY, "
        "case_id TEXT, "
        "party_number INTEGER, "
        "party_type TEXT, "
        "at_fault INTEGER, "
        "party_sex TEXT, "
        "party_age INTEGER, "
        "party_sobriety TEXT, "
        "party_drug_physical TEXT, "
        "direction_of_travel TEXT, "
        "party_safety_equipment_1 TEXT, "
        "party_safety_equipment_2 TEXT, "
        "financial_responsibility TEXT, "
        "hazardous_materials TEXT, "
        "cellphone_use TEXT, "
        "school_bus_related TEXT, "
        "oaf_violation_code TEXT, "
        "oaf_violation_category TEXT, "
        "oaf_violation_section INTEGER, "
        "oaf_violation_suffix TEXT, "
        "other_associate_factor_1 TEXT, "
        "other_associate_factor_2 TEXT, "
        "party_number_killed INTEGER, "
        "party_number_injured INTEGER, "
        "movement_preceding_collision TEXT, "
        "vehicle_year INTEGER, "
        "vehicle_make TEXT, "
        "statewide_vehicle_type TEXT, "
        "chp_vehicle_type_towing TEXT, "
        "chp_vehicle_type_towed TEXT, "
        "party_race TEXT"
        ")"
    )

def test_partyrow_columns():
    assert PartyRow.columns == [
        ("id", "INTEGER", "PRIMARY KEY"),
        ("case_id", "TEXT"),
        ("party_number", "INTEGER"),
        ("party_type", "TEXT"),
        ("at_fault", "INTEGER"),
        ("party_sex", "TEXT"),
        ("party_age", "INTEGER"),
        ("party_sobriety", "TEXT"),
        ("party_drug_physical", "TEXT"),
        ("direction_of_travel", "TEXT"),
        ("party_safety_equipment_1", "TEXT"),
        ("party_safety_equipment_2", "TEXT"),
        ("financial_responsibility", "TEXT"),
        ("hazardous_materials", "TEXT"),
        ("cellphone_use", "TEXT"),
        ("school_bus_related", "TEXT"),
        ("oaf_violation_code", "TEXT"),
        ("oaf_violation_category", "TEXT"),
        ("oaf_violation_section", "INTEGER"),
        ("oaf_violation_suffix", "TEXT"),
        ("other_associate_factor_1", "TEXT"),
        ("other_associate_factor_2", "TEXT"),
        ("party_number_killed", "INTEGER"),
        ("party_number_injured", "INTEGER"),
        ("movement_preceding_collision", "TEXT"),
        ("vehicle_year", "INTEGER"),
        ("vehicle_make", "TEXT"),
        ("statewide_vehicle_type", "TEXT"),
        ("chp_vehicle_type_towing", "TEXT"),
        ("chp_vehicle_type_towed", "TEXT"),
        ("party_race", "TEXT"),
    ]
