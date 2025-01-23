import re
from datetime import datetime, timedelta

from consts import max_day_range


def validate_date(date: str):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return False
    return True


def validate_date_argument(func):
    def wrapper(*args, **kwargs):
        if args:
            for i in range(2):
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', args[i]):
                    print('Wrong data format. At least one provided date does not match pattern YYYY-MM-DD.')
                    return False
        elif kwargs:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', kwargs['start_date']) or not re.match(r'^\d{4}-\d{2}-\d{2}$', kwargs['end_date']):
                print('Wrong data format. At least one provided date does not match pattern YYYY-MM-DD.')
                return False
        return func(*args, **kwargs)

    return wrapper


def calculate_working_dates(first: str, last: str) -> tuple:
    date_format = '%Y-%m-%d'

    first_date = datetime.strptime(first, date_format)
    while first_date.weekday() >= 5:
        first_date += timedelta(days=1)
    first_str = first_date.strftime(date_format)

    last_date = datetime.strptime(last, date_format)
    while last_date.weekday() >= 5:
        last_date -= timedelta(days=1)
    last_str = last_date.strftime(date_format)

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
