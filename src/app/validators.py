from datetime import datetime
from .dict_responses import invalid_clock_string


def is_valid_clock(time_clock_string: str):
    try:
        datetime.strptime(time_clock_string, '%H:%M')
    except ValueError as err:
        return invalid_clock_string()
    else:
        return time_clock_string
