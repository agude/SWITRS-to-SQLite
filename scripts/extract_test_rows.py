#!/usr/bin/env python3
"""Extract diverse test rows from real SWITRS data files.

This script analyzes large SWITRS CSV files and extracts a small set of
rows that maximize coverage of different value mappings and edge cases.

Usage:
    python scripts/extract_test_rows.py /tmp/CollisionRecords.txt /tmp/PartyRecords.txt /tmp/VictimRecords.txt
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

# Import value maps to know what we're looking for
sys.path.insert(0, str(Path(__file__).parent.parent))
from switrs_to_sqlite.value_maps import (
    COLLISION_SEVERITY,
    COLLISION_TYPE,
    DEGREE_OF_INJURY,
    DIRECTION,
    EJECTED,
    HIT_AND_RUN,
    INVOLVED_WITH,
    LIGHTING,
    MOVEMENT_PRECEDING,
    PARTY_TYPE,
    PEDESTRIAN_ACTION,
    PRIMARY_COLLISION_FACTOR,
    ROAD_SURFACE,
    ROLE,
    SAFETY,
    SEATING_POSITION,
    SEX,
    SOBRIETY,
    STATEWIDE_VEHICLE_TYPE,
    WEATHER,
)

# Column indices for key fields (0-indexed)
# These are the columns we want to maximize diversity on
COLLISION_KEY_COLUMNS = {
    "COLLISION_SEVERITY": 36,
    "WEATHER_1": 23,
    "WEATHER_2": 24,
    "TYPE_OF_COLLISION": 46,
    "HIT_AND_RUN": 45,
    "LIGHTING": 52,
    "ROAD_SURFACE": 49,
    "PRIMARY_COLL_FACTOR": 40,
    "PEDESTRIAN_ACCIDENT": 55,
    "BICYCLE_ACCIDENT": 56,
    "MOTORCYCLE_ACCIDENT": 57,
    "TRUCK_ACCIDENT": 58,
    "PED_ACTION": 48,
    "MVIW": 47,
}

PARTY_KEY_COLUMNS = {
    "PARTY_TYPE": 2,
    "PARTY_SEX": 4,
    "PARTY_SOBRIETY": 6,
    "DIR_OF_TRAVEL": 8,
    "MOVE_PRE_ACC": 23,
    "STWD_VEHICLE_TYPE": 26,
    "PARTY_SAFETY_EQUIP_1": 9,
    "RACE": 29,
}

VICTIM_KEY_COLUMNS = {
    "VICTIM_ROLE": 2,
    "VICTIM_SEX": 3,
    "VICTIM_DEGREE_OF_INJURY": 5,
    "VICTIM_SEATING_POSITION": 6,
    "VICTIM_EJECTED": 9,
}

# Value maps for each key column
COLLISION_VALUE_MAPS = {
    "COLLISION_SEVERITY": COLLISION_SEVERITY,
    "WEATHER_1": WEATHER,
    "WEATHER_2": WEATHER,
    "TYPE_OF_COLLISION": COLLISION_TYPE,
    "HIT_AND_RUN": HIT_AND_RUN,
    "LIGHTING": LIGHTING,
    "ROAD_SURFACE": ROAD_SURFACE,
    "PRIMARY_COLL_FACTOR": PRIMARY_COLLISION_FACTOR,
    "PED_ACTION": PEDESTRIAN_ACTION,
    "MVIW": INVOLVED_WITH,
}

PARTY_VALUE_MAPS = {
    "PARTY_TYPE": PARTY_TYPE,
    "PARTY_SEX": SEX,
    "PARTY_SOBRIETY": SOBRIETY,
    "DIR_OF_TRAVEL": DIRECTION,
    "MOVE_PRE_ACC": MOVEMENT_PRECEDING,
    "STWD_VEHICLE_TYPE": STATEWIDE_VEHICLE_TYPE,
    "PARTY_SAFETY_EQUIP_1": SAFETY,
}

VICTIM_VALUE_MAPS = {
    "VICTIM_ROLE": ROLE,
    "VICTIM_SEX": SEX,
    "VICTIM_DEGREE_OF_INJURY": DEGREE_OF_INJURY,
    "VICTIM_SEATING_POSITION": SEATING_POSITION,
    "VICTIM_EJECTED": EJECTED,
}


def analyze_file(filepath: str, key_columns: dict, value_maps: dict) -> dict:
    """Analyze a CSV file and find unique values for key columns."""
    print(f"\nAnalyzing: {filepath}")

    # Track: column -> value -> list of row indices
    value_occurrences: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )

    # Track all rows for later extraction
    all_rows: list[list[str]] = []
    header: list[str] = []

    with open(filepath, encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)

        for row_idx, row in enumerate(reader):
            all_rows.append(row)

            for col_name, col_idx in key_columns.items():
                if col_idx < len(row):
                    val = row[col_idx].strip()
                    if val:  # Only track non-empty values
                        value_occurrences[col_name][val].append(row_idx)

            # Progress indicator
            if row_idx % 500000 == 0 and row_idx > 0:
                print(f"  Processed {row_idx:,} rows...")

    print(f"  Total rows: {len(all_rows):,}")

    return {
        "header": header,
        "rows": all_rows,
        "occurrences": value_occurrences,
        "value_maps": value_maps,
    }


def print_coverage_report(data: dict, name: str) -> None:
    """Print a coverage report showing which values are present."""
    print(f"\n{'=' * 60}")
    print(f"Coverage Report: {name}")
    print("=" * 60)

    occurrences = data["occurrences"]
    value_maps = data["value_maps"]

    for col_name, found_values in sorted(occurrences.items()):
        expected_map = value_maps.get(col_name, {})

        print(f"\n{col_name}:")

        # Show found values
        found_codes = set(found_values.keys())
        expected_codes = set(expected_map.keys())

        # Values in data
        for code in sorted(found_codes):
            count = len(found_values[code])
            mapped = expected_map.get(code, "??? (unmapped)")
            in_expected = "✓" if code in expected_codes else "?"
            print(f"  {in_expected} '{code}' -> {mapped} ({count:,} rows)")

        # Missing values (in map but not in data)
        missing = expected_codes - found_codes
        if missing:
            print("  --- Not found in data ---")
            for code in sorted(missing):
                print(f"    '{code}' -> {expected_map[code]}")


def select_diverse_rows(data: dict, max_rows: int = 20) -> list[int]:
    """Select row indices that maximize value coverage."""
    # Track which values we've covered
    covered: dict[str, set[str]] = defaultdict(set)
    selected_rows: list[int] = []

    # Greedy selection: pick rows that cover the most new values
    all_row_indices = set(range(len(data["rows"])))

    while len(selected_rows) < max_rows and all_row_indices:
        best_row = None
        best_new_coverage = 0

        # Sample rows to check (checking all would be too slow)
        sample_size = min(10000, len(all_row_indices))
        sample = list(all_row_indices)[:sample_size]

        for row_idx in sample:
            new_coverage = 0
            row = data["rows"][row_idx]

            for col_name, col_idx in get_key_columns_for_data(data).items():
                if col_idx < len(row):
                    val = row[col_idx].strip()
                    if val and val not in covered[col_name]:
                        # Prefer values that are in the value map
                        if col_name in data["value_maps"]:
                            if val in data["value_maps"][col_name]:
                                new_coverage += 2  # Bonus for mapped values
                            else:
                                new_coverage += 1
                        else:
                            new_coverage += 1

            if new_coverage > best_new_coverage:
                best_new_coverage = new_coverage
                best_row = row_idx

        if best_row is None or best_new_coverage == 0:
            break

        # Add the best row
        selected_rows.append(best_row)
        all_row_indices.discard(best_row)

        # Update coverage
        row = data["rows"][best_row]
        for col_name, col_idx in get_key_columns_for_data(data).items():
            if col_idx < len(row):
                val = row[col_idx].strip()
                if val:
                    covered[col_name].add(val)

    return selected_rows


def get_key_columns_for_data(data: dict) -> dict:
    """Determine which key columns dict to use based on data."""
    header = data["header"]
    if "COLLISION_SEVERITY" in header:
        return COLLISION_KEY_COLUMNS
    elif "PARTY_TYPE" in header:
        return PARTY_KEY_COLUMNS
    else:
        return VICTIM_KEY_COLUMNS


def extract_rows(data: dict, row_indices: list[int]) -> list[str]:
    """Extract rows as CSV strings."""
    rows = []
    for idx in row_indices:
        row = data["rows"][idx]
        # Convert back to CSV format
        csv_row = ",".join(
            f'"{val}"' if "," in val or '"' in val else val for val in row
        )
        rows.append(csv_row)
    return rows


def main():
    if len(sys.argv) != 4:
        print("Usage: python extract_test_rows.py <collisions> <parties> <victims>")
        sys.exit(1)

    collision_file, party_file, victim_file = sys.argv[1:4]

    # Analyze each file
    collision_data = analyze_file(
        collision_file, COLLISION_KEY_COLUMNS, COLLISION_VALUE_MAPS
    )
    party_data = analyze_file(party_file, PARTY_KEY_COLUMNS, PARTY_VALUE_MAPS)
    victim_data = analyze_file(victim_file, VICTIM_KEY_COLUMNS, VICTIM_VALUE_MAPS)

    # Print coverage reports
    print_coverage_report(collision_data, "Collisions")
    print_coverage_report(party_data, "Parties")
    print_coverage_report(victim_data, "Victims")

    # Select diverse rows
    print("\n" + "=" * 60)
    print("Selecting diverse rows...")
    print("=" * 60)

    collision_indices = select_diverse_rows(collision_data, max_rows=15)
    party_indices = select_diverse_rows(party_data, max_rows=20)
    victim_indices = select_diverse_rows(victim_data, max_rows=15)

    # Get case_ids from selected collision rows to find related parties/victims
    selected_case_ids = set()
    for idx in collision_indices:
        case_id = collision_data["rows"][idx][0].strip('"')
        selected_case_ids.add(case_id)

    print(f"\nSelected {len(collision_indices)} collision rows")
    print(f"Selected {len(party_indices)} party rows")
    print(f"Selected {len(victim_indices)} victim rows")
    print(f"Case IDs: {selected_case_ids}")

    # Output the selected rows
    print("\n--- Selected Collision Rows ---")
    collision_rows = extract_rows(collision_data, collision_indices)
    for row in collision_rows:
        print(row)

    print("\n--- Selected Party Rows ---")
    party_rows = extract_rows(party_data, party_indices)
    for row in party_rows:
        print(row)

    print("\n--- Selected Victim Rows ---")
    victim_rows = extract_rows(victim_data, victim_indices)
    for row in victim_rows:
        print(row)

    # Also find parties and victims that match the selected collision case_ids
    print("\n--- Parties matching selected collisions ---")
    for idx, row in enumerate(party_data["rows"]):
        case_id = row[0].strip('"')
        if case_id in selected_case_ids:
            print(extract_rows(party_data, [idx])[0])

    print("\n--- Victims matching selected collisions ---")
    for idx, row in enumerate(victim_data["rows"]):
        case_id = row[0].strip('"')
        if case_id in selected_case_ids:
            print(extract_rows(victim_data, [idx])[0])


if __name__ == "__main__":
    main()
