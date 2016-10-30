#!/usr/bin/env python3

from switrs_to_sqlite.switrs_to_sqlite import VictimRow
import pytest

# A list of tuples, with each tuple containing a row ready to be parsed, and
# the answer that should be returned from doing so. The tuple is of the form
# (row, answer)
ROWS = (
    (
        #      Case_ID     Party_Number  Victim_Role  Victim_Sex  Victim_Age  Victim_Degree_Of_Injury  Victim_Seating_Position  Victim_Safety_Equipment_1  Victim_Safety_Equipment_2  Victim_Ejected
        [      '097293',   '1',          '2',         'M',        '20',       '0',                     '3',                     'G',                       'T',                       '0'],
        [None, '097293',   1,            '2',         'M',        20,         '0',                     '3',                     'G',                       'T',                       '0'],
    ),
    (
        #      Case_ID     Party_Number  Victim_Role  Victim_Sex  Victim_Age  Victim_Degree_Of_Injury  Victim_Seating_Position  Victim_Safety_Equipment_1  Victim_Safety_Equipment_2  Victim_Ejected
        [      '965874',   '2',          '2',         '-',        '998',      '2',                     'A',                     '-',                       '-',                       '2'],
        [None, '965874',   2,            '2',         None,       None,       '2',                     'A',                     None,                      None,                      '2'],
    ),
    (
        #      Case_ID     Party_Number  Victim_Role  Victim_Sex  Victim_Age  Victim_Degree_Of_Injury  Victim_Seating_Position  Victim_Safety_Equipment_1  Victim_Safety_Equipment_2  Victim_Ejected
        [      '0000003',  '6',          '2',         'F',        '999',      '1',                     '3',                     'T',                       '-',                       '-'],
        [None, '0000003',  6,            '2',         'F',        999,        '1',                     '3',                     'T',                       None,                      None],
    ),
)


def test_victimrows():
    for row, answer in ROWS:
        c = VictimRow(row)
        assert c.values == answer
