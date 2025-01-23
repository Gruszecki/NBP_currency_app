import re
from datetime import datetime, timedelta

from consts import max_day_range


def validate_dates(dates: list[str]):
    for date in dates:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            return False
    return True


def validate_dates_argument(func):
    def wrapper(*args, **kwargs):
        for date in args[0]:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
                print('Wrong data format. At least one provided date does not match pattern YYYY-MM-DD.')
                return False
        return func(*args, **kwargs)
    return wrapper


def calculate_working_dates(dates: list[str] | tuple) -> tuple:
    date_format = '%Y-%m-%d'

    first = datetime.strptime(dates[0], date_format)
    while first.weekday() >= 5:
        first += timedelta(days=1)
    first_str = first.strftime(date_format)

    last = datetime.strptime(dates[1], date_format)
    while last.weekday() >= 5:
        last -= timedelta(days=1)
    last_str = last.strftime(date_format)

    return first_str, last_str


def identify_date_ranges(start_date: str, end_date: str) -> list[tuple]:
    """
    Identify and generate a list of date ranges between the start and end dates.

    This method calculates contiguous date ranges with a maximum range of `max_day_range` which is defined by NBP
    as maximal time range for API.

    Returns:
        list[tuple]: A list of tuples where each tuple contains two strings:
                     - The start date of the range (inclusive).
                     - The end date of the range (inclusive).
                     Example: [("2020-01-17", "2020-04-19"), ("2020-04-20", "2020-04-20")].

    Notes:
        The `start` and `end` attributes are expected to be strings in "YYYY-MM-DD" format.
    """
    date_format = '%Y-%m-%d'
    first = datetime.strptime(start_date, date_format)
    last = datetime.strptime(end_date, date_format)
    days_delta = timedelta(days=max_day_range)
    ranges = []

    while first <= last:
        if first + days_delta < last:
            ranges.append((first.strftime(date_format), (first + days_delta).strftime(date_format)))
        else:
            ranges.append((first.strftime(date_format), last.strftime(date_format)))
        first += days_delta + timedelta(days=1)

    return ranges
