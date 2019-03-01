def convert(**kwargs):
    """Convert a value to a dtype, but turn certain values to None.

    Convert calls val.strip() before performing any other work.

    Args:
        **kwargs: Two specific keywords must be passed, a third is optional:
            - val (str): A value to convert to dtype.
            - dtype (callable): A callable object that returns the desired
                type, if None then the val is passed through unchanged.
            - nulls (iterable, optional): An iterable containing strings to check
                against. If val if found to be equal to a string in this list,
                None is returned.

    Returns:
        converted_val: Returns dtype(val) if val is not in nulls, otherwise
            None. If dtype(val) raises a ValueError, None is returned.
    """
    # Get the arguments
    val = kwargs.get("val")
    dtype = kwargs.get("dtype")
    nulls = kwargs.get("nulls", None)

    # Strip spaces
    sval = val.strip()

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


def negative(**kwargs):
    """Use convert() to convert a value, and then return it multiplied by -1.

    This function uses convert() to perform the conversion and so passes
    through all arguments. If convert() returns None, than this function will
    also.

    Args:
        **kwargs: Two specific keywords must be passed, a third is optional:
            - val (str): A value to convert to dtype.
            - dtype (callable): A callable object that returns the desired
                type, if None then the val is passed through unchanged. The
                returned object should allow multiplication by -1, or None will
                be returned instead.
            - nulls (iterable, optional): An iterable containing strings to check
                against. If val if found to be equal to a string in this list,
                None is returned.

    Returns:
        converted_val: Returns -1 * convert(kwargs), unless convert() returns
            None, in which case None is returned.
    """
    # Use convert to do the conversion
    out_val = convert(**kwargs)

    # If convert succeeded, return the value times -1
    if out_val is not None:
        return -1 * out_val

    return None


def string_to_bool(**kwargs):
    """Convert Y/N or y/n to a True/False, or None if in a list of nulls.

    Args:
        **kwargs: One specific keywords must be passed, a second is optional:
            - val (str): A value to convert to a bool.
            - nulls (iterable, optional): An iterable containing strings to check
                against. If val if found to be equal to a string in this list,
                None is returned.

    Returns:
        converted_val: Returns a bool if val is not in nulls, otherwise None.

    """
    # Get the arguments
    val = kwargs.get("val")
    nulls = kwargs.get("nulls", None)

    # Return None if the val matches a string in nulls
    if nulls is not None:
        if val in nulls:
            return None

    # Check if val is True, otherwise return False
    if val.lower() == "y":
        return True
    return False
