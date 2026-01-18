"""Converter functions for transforming CSV values to database values."""

from collections.abc import Collection


def identity(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> str:
    """Return the value unchanged. Default converter when no transformation needed."""
    return val


def convert(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> str | int | float | None:
    """Convert a value to a dtype, but turn certain values to None.

    Convert calls val.strip() before performing any other work.

    Args:
        val: A value to convert to dtype.
        dtype: A callable object that returns the desired type, if None then
            the val is passed through unchanged.
        nulls: An iterable containing strings to check against. If val is
            found to be equal to a string in this list, None is returned.

    Returns:
        Returns dtype(val) if val is not in nulls, otherwise None.
        If dtype(val) raises a ValueError, None is returned.
    """
    # Strip spaces
    sval: str = val.strip()

    # Return None if the val matches a string in nulls
    if nulls is not None:
        if sval in nulls:
            return None

    # Otherwise return the converted value
    if dtype is not None:
        try:
            return dtype(sval)
        except ValueError:
            return None
    # Note: val and not sval because this is the identity operation
    else:
        return val


def negative(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> int | float | None:
    """Use convert() to convert a value, and then return it multiplied by -1.

    This function uses convert() to perform the conversion and so passes
    through all arguments. If convert() returns None, then this function will
    also.

    Args:
        val: A value to convert to dtype.
        dtype: A callable object that returns the desired type, if None then
            the val is passed through unchanged. The returned object should
            allow multiplication by -1, or None will be returned instead.
        nulls: An iterable containing strings to check against. If val is
            found to be equal to a string in this list, None is returned.

    Returns:
        Returns -1 * convert(val, dtype, nulls), unless convert() returns
        None or a non-numeric type, in which case None is returned.
    """
    # Use convert to do the conversion
    out_val = convert(val, dtype, nulls)

    # If convert succeeded with a numeric type, return the value times -1
    if isinstance(out_val, (int, float)):
        return -1 * out_val

    return None


def string_to_bool(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> bool | None:
    """Convert Y/N or y/n to a True/False, or None if in a list of nulls.

    Args:
        val: A value to convert to a bool.
        dtype: Unused, included for consistent converter signature.
        nulls: An iterable containing strings to check against. If val is
            found to be equal to a string in this list, None is returned.

    Returns:
        Returns a bool if val is not in nulls, otherwise None.
    """
    # Return None if the val matches a string in nulls
    if nulls is not None:
        if val in nulls:
            return None

    # Check if val is True, otherwise return False
    if val.lower() == "y":
        return True
    return False


def county_city_location_to_county(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> str | None:
    """Convert a 4-digit county-city location code to a county code.

    The county-city codes are four digits, like XXYY. The county code is just
    the first two digits, so XX in this example. The codes are not numbers,
    leading zeros need to be preserved.

    Args:
        val: A value to convert to a county code.
        dtype: Passed to convert() for type conversion.
        nulls: An iterable containing strings to check against. If val is
            found to be equal to a string in this list, None is returned.

    Returns:
        Returns a county code string if val is not in nulls, otherwise None.
    """
    # Use convert to do the conversion
    out_val = convert(val, dtype, nulls)

    if out_val is None:
        return None

    return str(out_val)[:2]


def cellphone_use_to_bool(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> bool | None:
    """A cellphone use code to True/False if a cellphone was in use.

    The mapping is:

    B -> cellphone in use              -> True
    C -> cellphone not in use          -> False
    D -> no cellphone/unknown          -> None
    1 -> cellphone in use (handheld)   -> True
    2 -> cellphone in use (hands-free) -> True
    3 -> cellphone not in use          -> False

    Args:
        val: A value to convert to a bool.
        dtype: Unused, included for consistent converter signature.
        nulls: An iterable containing strings to check against. If val is
            found to be equal to a string in this list, None is returned.

    Returns:
        Returns a bool if val is not in nulls, otherwise None.
    """
    # Return None if the val matches a string in nulls
    if nulls is not None:
        if val in nulls:
            return None

    # Map val
    CELLPHONE_IN_USE: dict[str, bool | None] = {
        "B": True,
        "C": False,
        "D": None,
        "1": True,
        "2": True,
        "3": False,
    }

    return CELLPHONE_IN_USE.get(val, None)


def non_standard_str_to_bool(
    val: str,
    dtype: type[int] | type[float] | type[str] | None = None,
    nulls: Collection[str] | None = None,
) -> bool | None:
    """Convert a hard-coded set of keys to bools, everything else to None.

    Args:
        val: A value to convert to a bool.
        dtype: Unused, included for consistent converter signature.
        nulls: An iterable containing strings to check against. If val is
            found to be equal to a string in this list, None is returned.

    Returns:
        Returns a bool if val is not in nulls, otherwise None.
    """
    # Return None if the val matches a string in nulls
    if nulls is not None:
        if val in nulls:
            return None

    # Map val
    MAP: dict[str, bool] = {
        # Parties: hazardous_materials
        "A": True,
        # Parties: school_bus_related
        "E": True,
    }

    return MAP.get(val, None)
