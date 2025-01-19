import re
import requests
from datetime import datetime, timedelta
from pprint import pprint

from consts import api_table_a, max_day_range


class Data:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start = start_date
        self.end = end_date
        self.data = []

        self._get_data_range()

    def _get_data_range(self) -> None:
        """Retrieve data from NBP API for time range specified within class instance."""
        ranges = self._identify_date_ranges()

        for ran in ranges:
            try:
                response = requests.get(f'{api_table_a}/{ran[0]}/{ran[1]}')
                self.data.extend(response.json())
            except requests.exceptions.JSONDecodeError:
                print("Given time range exceeds available data.")
                return None

    def _identify_date_ranges(self) -> list[tuple]:
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
        first = datetime(*map(int, self.start.split('-')))
        last = datetime(*map(int, self.end.split('-')))

        days_delta = timedelta(days=max_day_range)
        date_format = '%Y-%m-%d'
        ranges = []

        while first <= last:
            if first + days_delta < last:
                ranges.append((first.strftime(date_format), (first + days_delta).strftime(date_format)))
            else:
                ranges.append((first.strftime(date_format), last.strftime(date_format)))
            first += days_delta + timedelta(days=1)

        return ranges

    def show_data(self) -> None:
        pprint(self.data)

    def analyze_max_inc_dec(self):
        """
        Analyze the maximum increase and decrease in currency exchange rates over a specified period.

        Returns:
            tuple: A tuple containing:
                - max_inc (tuple): The maximum increase as a tuple of the increase value (float) and
                  the currency code (str). Example: (1.25, 'USD').
                - max_dec (tuple): The maximum decrease as a tuple of the decrease value (float) and
                  the currency code (str). Example: (-0.75, 'EUR').
        """
        first = self.data[0]['rates']
        last = self.data[len(self.data)-1]['rates']
        last_d = {record['code']: record['mid'] for record in last}

        max_dec = (999, '')
        max_inc = (0, '')

        for first_d in first:
            val_last = last_d.get(first_d['code'], 0)

            if val_last:
                diff = val_last - first_d['mid']
                if diff > max_inc[0]:
                    max_inc = (diff, first_d['code'])
                if diff < max_dec[0]:
                    max_dec = (diff, first_d['code'])

        return max_inc, max_dec

    @staticmethod
    def validate_date(date: str) -> bool:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            return False
        return True