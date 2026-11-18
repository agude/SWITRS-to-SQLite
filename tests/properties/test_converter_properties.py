"""Model-based properties for SWITRS value converters."""

from datetime import date, time

from hypothesis import event, example, given
from hypothesis import strategies as st

from switrs_to_sqlite.converters import (
    cellphone_use_to_bool,
    convert,
    convert_date,
    convert_time,
    negative,
    non_standard_str_to_bool,
)


@st.composite
def eight_digit_dates(draw: st.DrawFn) -> str:
    """Generate YYYYMMDD-shaped values, including invalid calendar dates."""
    return "".join(draw(st.lists(st.sampled_from("0123456789"), min_size=8, max_size=8)))


@st.composite
def four_digit_times(draw: st.DrawFn) -> str:
    """Generate HHMM-shaped values, including invalid clock times."""
    return "".join(draw(st.lists(st.sampled_from("0123456789"), min_size=4, max_size=4)))


@given(
    st.one_of(eight_digit_dates(), st.dates().map(lambda value: value.isoformat().replace("-", "")))
)
@example("20000229")
@example("19000229")
def test_convert_date_matches_calendar_constructor(value: str) -> None:
    year, month, day = int(value[:4]), int(value[4:6]), int(value[6:])
    try:
        expected = date(year, month, day).isoformat()
    except ValueError:
        expected = None

    event(f"valid calendar date: {expected is not None}")
    assert convert_date(value) == expected


@given(four_digit_times())
@example("0000")
@example("2359")
@example("2400")
@example("2500")
@example("0060")
def test_convert_time_matches_clock_constructor(value: str) -> None:
    hour, minute = int(value[:2]), int(value[2:])
    try:
        expected = time(hour, minute).isoformat()
    except ValueError:
        expected = None

    event(f"valid clock time: {expected is not None}")
    assert convert_time(value) == expected


@given(hour=st.integers(0, 9), minute=st.integers(0, 59))
def test_convert_time_accepts_unpadded_hours(hour: int, minute: int) -> None:
    assert convert_time(f"{hour}{minute:02d}") == time(hour, minute).isoformat()


@given(st.integers(min_value=-(2**63), max_value=2**63 - 1))
def test_numeric_conversion_and_negative_preserve_integer_value(value: int) -> None:
    token = str(value)

    assert convert(token, int) == value
    assert negative(token, int) == -abs(value)


@given(st.floats(allow_nan=False, allow_infinity=False, width=32))
def test_numeric_conversion_and_negative_preserve_finite_float(value: float) -> None:
    token = repr(value)

    assert convert(token, float) == value
    assert negative(token, float) == -abs(value)


@given(st.sampled_from(["", " ", "NA", "N/A", "null"]))
def test_configured_sentinels_are_null_after_whitespace_stripping(value: str) -> None:
    assert convert(value, int, nulls=("", "NA", "N/A", "null")) is None
    assert negative(value, int, nulls=("", "NA", "N/A", "null")) is None
    assert convert_date(value, nulls=("", "NA", "N/A", "null")) is None
    assert convert_time(value, nulls=("", "NA", "N/A", "null")) is None


@given(st.text(alphabet="0123456789", min_size=5, max_size=7))
def test_date_and_time_reject_incomplete_date_fields(value: str) -> None:
    assert convert_date(value) is None
    assert convert_time(value) is None


@given(
    code=st.sampled_from(["", "1", "2", "3", "A", "B", "C", "D", "E", "b", "X"]),
    nulls=st.sets(st.sampled_from(["", "1", "2", "3", "A", "B", "C", "D", "E"])),
    padding=st.text(alphabet=" \t", max_size=4),
)
def test_boolean_codes_apply_nulls_before_lookup(code: str, nulls: set[str], padding: str) -> None:
    cellphone_codes = {"1": True, "2": True, "3": False, "B": True, "C": False}
    nonstandard_codes = {"A": True, "E": True}
    token = f"{padding}{code}{padding}"

    assert cellphone_use_to_bool(token, nulls=nulls) is (
        None if code in nulls else cellphone_codes.get(code)
    )
    assert non_standard_str_to_bool(token, nulls=nulls) is (
        None if code in nulls else nonstandard_codes.get(code)
    )
