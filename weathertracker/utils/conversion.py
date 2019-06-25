from dateutil.parser import parse


class DatetimeConversionException(Exception):
    pass


def convert_to_datetime(value):
    try:
        value = parse(value)
    except (ValueError, OverflowError):
        raise DatetimeConversionException()
    return value


def convert_to_string(value):
    try:
        value = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    except ValueError:
        raise DatetimeConversionException()
    return value
