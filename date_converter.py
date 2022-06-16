import math
import datetime
from dateparser import parse

DateTypes = str | int | float | datetime.date
TIMESTAMP_DIGITS = 10
PARSER_SETTINGS = {
    "TIMEZONE": "UTC",
    "PREFER_DAY_OF_MONTH": "first",
    "RETURN_AS_TIMEZONE_AWARE": True
}


def date_to(your_date: DateTypes, end_type: DateTypes) -> DateTypes:
    """

    :param your_date: Requires to be either int, float, str, or datetime.date
    :param end_type: The type you want the date to be converted into
    :return: converted time to specified Type[end_type] rounded to seconds and always in UTC
    """
    
    if isinstance(end_type, str):
        match end_type.lower():
            case "timestamp" | "epoch" | "int" | "unix":
                end_type = int
            case "datetime" | "datetime.time" | "date":
                end_type = datetime.date
            case "str" | "string":
                end_type = str
            case _:
                raise TypeError(f"The only date types allowed are {DateTypes} "
                                f"or one of the strings 'timestamp', 'epoch', 'datetime'")
    
    if not your_date:
        return your_date
    elif isinstance(your_date, int):
        your_date = _round_timestamp_to_seconds(your_date)


    if end_type == datetime.date:
        your_date = _to_datetime(your_date)
    
    elif end_type == int:
        if isinstance(your_date, str):
            your_date = _string_date_to_timestamp(your_date)
        elif isinstance(your_date, datetime.date):
            your_date = _date_time_to_timestamp(your_date)
        elif isinstance(your_date, float):
            your_date = int(your_date)
    
    elif end_type == str:
        if isinstance(your_date, str):
            # This operation completes a possibly incomplete query_string to the second
            your_date = _to_datetime(your_date)
        elif isinstance(your_date, (int, float)):
            your_date = _to_datetime(your_date)
        your_date = your_date.isoformat()

    return your_date


def _to_datetime(_time: DateTypes) -> datetime.date:
    if not isinstance(_time, (int, float)):
        if isinstance(_time, str):
            _time = parse(_time, settings=PARSER_SETTINGS)
        _time = _date_time_to_timestamp(_time)
    return datetime.datetime.fromtimestamp(_time, tz=datetime.timezone.utc)


def _round_timestamp_to_seconds(_timestamp: int) -> int:  # Assumes positive number
    stamp_digits = TIMESTAMP_DIGITS
    num_length = int(math.log10(_timestamp)) + 1
    if num_length > stamp_digits:
        decimal = num_length - stamp_digits
        _timestamp //= 10 ** decimal
    return _timestamp


def _date_time_to_timestamp(_date_time) -> int:
    """ Issue:https://stackoverflow.com/questions/60736569/timestamp-subtraction-must-have-the-same-timezones-or-no-timezones-but-they-are """
    _date_time = _date_time.replace(tzinfo=datetime.timezone.utc)  # pd.to_datetime uses pytz, can result in conflict
    unix_start = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
    return int((_date_time - unix_start).total_seconds())


def _string_date_to_timestamp(date_string: str) -> int:
    date_time = _to_datetime(date_string)
    return _date_time_to_timestamp(date_time)
