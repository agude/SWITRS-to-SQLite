#!/usr/bin/env python3

from switrs_to_sqlite.parsers import VictimRow


# A list of tuples, with each tuple containing a row ready to be parsed, and
# the answer that should be returned from doing so. The tuple is of the form
# (row, answer)
ROWS = (
    (
        #      Case_ID     Party_Number  Victim_Role   Victim_Sex  Victim_Age  Victim_Degree_Of_Injury  Victim_Seating_Position  Victim_Safety_Equipment_1     Victim_Safety_Equipment_2                    Victim_Ejected
        [      '097293',   '1',          '5',          'M',        '20',       '0',                     '3',                     'G',                          'T',                                         '0'],
        [None, '097293',   1,            'other',      'male',     20,         'no injury',             'passenger seat 3',      'lap/shoulder harness used',  'child restraint in vehicle, improper use',  'not ejected'],
    ),
    (
        #      Case_ID     Party_Number  Victim_Role   Victim_Sex  Victim_Age  Victim_Degree_Of_Injury  Victim_Seating_Position  Victim_Safety_Equipment_1     Victim_Safety_Equipment_2                    Victim_Ejected
        [      '965874',   '2',          '2',          '-',        '998',      '-',                     'A',                     '-',                          '-',                                         '2'],
        [None, '965874',   2,            'passenger',  None,       None,       None,                    'A',                     None,                         None,                                        'partially ejected'],
    ),
    (
        #      Case_ID     Party_Number  Victim_Role   Victim_Sex  Victim_Age  Victim_Degree_Of_Injury  Victim_Seating_Position  Victim_Safety_Equipment_1     Victim_Safety_Equipment_2                    Victim_Ejected
        [      '0000003',  '6',          '1',          'F',        '999',      '7',                     '1',                     'C',                          '-',                                         '-'],
        [None, '0000003',  6,            'driver',     'female',   999,        'possible injury',       'driver',                'lap belt used',              None,                                        None],
    ),
)


def test_victimrows():
    for row, answer in ROWS:
        parsed_row = VictimRow.parse_row(row)
        assert parsed_row == answer

def test_vicitimrow_create_table():
    assert VictimRow.create_table_statement() == (
        "CREATE TABLE "
        "victims ("
        "id INTEGER PRIMARY KEY, "
        "case_id TEXT, "
        "party_number INTEGER, "
        "victim_role TEXT, "
        "victim_sex TEXT, "
        "victim_age INTEGER, "
        "victim_degree_of_injury TEXT, "
        "victim_seating_position TEXT, "
        "victim_safety_equipment_1 TEXT, "
        "victim_safety_equipment_2 TEXT, "
        "victim_ejected TEXT"
        ")"
    )

def test_victimrow_columns():
    assert VictimRow.columns == [
        ("id", "INTEGER", "PRIMARY KEY"),
        ("case_id", "TEXT"),
        ("party_number", "INTEGER"),
        ("victim_role", "TEXT"),
        ("victim_sex", "TEXT"),
        ("victim_age", "INTEGER"),
        ("victim_degree_of_injury", "TEXT"),
        ("victim_seating_position", "TEXT"),
        ("victim_safety_equipment_1", "TEXT"),
        ("victim_safety_equipment_2", "TEXT"),
        ("victim_ejected", "TEXT"),
    ]
