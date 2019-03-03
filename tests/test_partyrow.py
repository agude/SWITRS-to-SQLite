#!/usr/bin/env python3

from switrs_to_sqlite.switrs_to_sqlite import PartyRow
import pytest

# A list of tuples, with each tuple containing a row ready to be parsed, and
# the answer that should be returned from doing so. The tuple is of the form
# (row, answer)
ROWS = (
    (
        #      Case_ID     Party_Number  Party_Type  At_Fault  Party_Sex  Party_Age  Party_Sobriety  Party_Drug_Physical  Direction_Of_Travel  Party_Safety_Equipment_1  Party_Safety_Equipment_2  Financial_Responsibility  Hazardous_Materials  Cellphone_Use  School_Bus_Related  OAF_Violation_Code  OAF_Violation_Category  OAF_Violation_Section  OAF_Violation_Suffix  Other_Associate_Factor_1  Other_Associate_Factor_2  Party_Number_Killed  Party_Number_Injured  Movement_Preceding_Collision  Vehicle_Year  Vehicle_Make  Statewide_Vehicle_Type  CHP_Vehicle_Type_Towing  CHP_Vehicle_Type_Towed  Party_Race
        [      '097293',   '1',          '1',        'Y',      'M',       '20',      'A',            'H',                 'E',                 'A',                      'F',                      'N',                      'A',                 'D',           'E',                'C',                '18',                   '12345',               'A',                  'N',                      'A',                      '0',                 '0',                  'M',                          '1996',       'FORD',       'A',                    '08',                    '00',                   'W'],
        [None, '097293',   1,            '1',        True,     'M',       20,        'A',            'H',                 'E',                 'A',                      'F',                      'N',                      'A',                 'D',           'E',                'C',                '18',                   12345,                 'A',                  'N',                      'A',                      0,                   0,                    'M',                          1996,         'FORD',       'A',                    '08',                    '00',                   'W',],
    ),
    (
        #      Case_ID     Party_Number  Party_Type  At_Fault  Party_Sex  Party_Age  Party_Sobriety  Party_Drug_Physical  Direction_Of_Travel  Party_Safety_Equipment_1  Party_Safety_Equipment_2  Financial_Responsibility  Hazardous_Materials  Cellphone_Use  School_Bus_Related  OAF_Violation_Code  OAF_Violation_Category  OAF_Violation_Section  OAF_Violation_Suffix  Other_Associate_Factor_1  Other_Associate_Factor_2  Party_Number_Killed  Party_Number_Injured  Movement_Preceding_Collision  Vehicle_Year  Vehicle_Make  Statewide_Vehicle_Type  CHP_Vehicle_Type_Towing  CHP_Vehicle_Type_Towed  Party_Race
        [      '0018200',  '3',          '4',        'N',      'F',       '999',     'H',            'E',                 'N',                 'G',                      '-',                      'Y',                      '-',                 'B',           '-',                'W',                '29',                   '',                    'B',                  'G',                      '-',                      '1',                 '1',                  'A',                          '1987',       'BMW',        'O',                    '97',                    '98',                   'H'],
        [None, '0018200',  3,            '4',        False,    'F',       999,       'H',            'E',                 'N',                 'G',                      None,                     'Y',                      None,                'B',           None,               'W',                '29',                   None,                  'B',                  'G',                      None,                     1,                   1,                    'A',                          1987,         'BMW',        'O',                    '97',                    '98',                   'H',],
    ),
    (
        #      Case_ID     Party_Number  Party_Type  At_Fault  Party_Sex  Party_Age  Party_Sobriety  Party_Drug_Physical  Direction_Of_Travel  Party_Safety_Equipment_1  Party_Safety_Equipment_2  Financial_Responsibility  Hazardous_Materials  Cellphone_Use  School_Bus_Related  OAF_Violation_Code  OAF_Violation_Category  OAF_Violation_Section  OAF_Violation_Suffix  Other_Associate_Factor_1  Other_Associate_Factor_2  Party_Number_Killed  Party_Number_Injured  Movement_Preceding_Collision  Vehicle_Year  Vehicle_Make  Statewide_Vehicle_Type  CHP_Vehicle_Type_Towing  CHP_Vehicle_Type_Towed  Party_Race
        [      '0036598',  '2',          '-',        '-',      '-',       '998',     '-',            '-',                 '-',                 '-',                      '-',                      '',                       '-',                 '-',           '-',                '-',                '00',                   '',                    '',                   '-',                      '-',                      '20',                '2',                  '-',                          '9999',       'PONTIAC',    '-',                    '99',                    '99',                   ''],
        [None, '0036598',  2,            None,       None,     None,      None,      None,           None,                None,                None,                     None,                     None,                     None,                None,          None,               None,               None,                   None,                  None,                 None,                     None,                     20,                  2,                    None,                         None,         'PONTIAC',    None,                   None,                    None,                   None],
    ),
)


def test_partyrows():
    for row, answer in ROWS:
        parsed_row = PartyRow.parse_row(row)
        assert parsed_row == answer

def test_partyrow_create_table():
    assert PartyRow.create_table_statement() == (
        "CREATE TABLE "
        "Party ("
        "id INTEGER PRIMARY KEY, "
        "Case_ID TEXT, "
        "Party_Number INTEGER, "
        "Party_Type TEXT, "
        "At_Fault TEXT, "
        "Party_Sex TEXT, "
        "Party_Age INTEGER, "
        "Party_Sobriety TEXT, "
        "Party_Drug_Physical TEXT, "
        "Direction_Of_Travel TEXT, "
        "Party_Safety_Equipment_1 TEXT, "
        "Party_Safety_Equipment_2 TEXT, "
        "Financial_Responsibility TEXT, "
        "Hazardous_Materials TEXT, "
        "Cellphone_Use TEXT, "
        "School_Bus_Related TEXT, "
        "OAF_Violation_Code TEXT, "
        "OAF_Violation_Category TEXT, "
        "OAF_Violation_Section INTEGER, "
        "OAF_Violation_Suffix TEXT, "
        "Other_Associate_Factor_1 TEXT, "
        "Other_Associate_Factor_2 TEXT, "
        "Party_Number_Killed INTEGER, "
        "Party_Number_Injured INTEGER, "
        "Movement_Preceding_Collision TEXT, "
        "Vehicle_Year INTEGER, "
        "Vehicle_Make TEXT, "
        "Statewide_Vehicle_Type TEXT, "
        "CHP_Vehicle_Type_Towing TEXT, "
        "CHP_Vehicle_Type_Towed TEXT, "
        "Party_Race TEXT"
        ")"
    )

def test_partyrow_columns():
    assert PartyRow.columns == [
        ("id", "INTEGER", "PRIMARY KEY"),
        ("Case_ID", "TEXT"),
        ("Party_Number", "INTEGER"),
        ("Party_Type", "TEXT"),
        ("At_Fault", "TEXT"),
        ("Party_Sex", "TEXT"),
        ("Party_Age", "INTEGER"),
        ("Party_Sobriety", "TEXT"),
        ("Party_Drug_Physical", "TEXT"),
        ("Direction_Of_Travel", "TEXT"),
        ("Party_Safety_Equipment_1", "TEXT"),
        ("Party_Safety_Equipment_2", "TEXT"),
        ("Financial_Responsibility", "TEXT"),
        ("Hazardous_Materials", "TEXT"),
        ("Cellphone_Use", "TEXT"),
        ("School_Bus_Related", "TEXT"),
        ("OAF_Violation_Code", "TEXT"),
        ("OAF_Violation_Category", "TEXT"),
        ("OAF_Violation_Section", "INTEGER"),
        ("OAF_Violation_Suffix", "TEXT"),
        ("Other_Associate_Factor_1", "TEXT"),
        ("Other_Associate_Factor_2", "TEXT"),
        ("Party_Number_Killed", "INTEGER"),
        ("Party_Number_Injured", "INTEGER"),
        ("Movement_Preceding_Collision", "TEXT"),
        ("Vehicle_Year", "INTEGER"),
        ("Vehicle_Make", "TEXT"),
        ("Statewide_Vehicle_Type", "TEXT"),
        ("CHP_Vehicle_Type_Towing", "TEXT"),
        ("CHP_Vehicle_Type_Towed", "TEXT"),
        ("Party_Race", "TEXT"),
    ]
