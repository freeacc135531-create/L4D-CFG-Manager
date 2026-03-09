def _validate_number(value, cast_type, min_val=None, max_val=None):
    try:
        val = cast_type(value)

        if min_val is not None and val < min_val:
            return False, f"Value must be >= {min_val}"

        if max_val is not None and val > max_val:
            return False, f"Value must be <= {max_val}"

        return True, ""

    except (ValueError, TypeError):
        type_name = "integer" if cast_type is int else "number"
        return False, f"Invalid {type_name}"


def validate_numeric(value, min_val=None, max_val=None):
    """
    Validate a float value.
    """
    return _validate_number(value, float, min_val, max_val)


def validate_int(value, min_val=None, max_val=None):
    """
    Validate an integer value.
    """
    return _validate_number(value, int, min_val, max_val)