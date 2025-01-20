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
        date_format = '%Y-%m-%d'
        first = datetime.strptime(self.start, date_format)
        last = datetime.strptime(self.end, date_format)
        days_delta = timedelta(days=max_day_range)
        ranges = []

        while first <= last:
            if first + days_delta < last:
                ranges.append((first.strftime(date_format), (first + days_delta).strftime(date_format)))
            else:
                ranges.append((first.strftime(date_format), last.strftime(date_format)))
            first += days_delta + timedelta(days=1)

        return ranges

    def get_data_in_range(self) -> bool:
        """Retrieve data from NBP API for time range specified within class instance."""
        ranges = self._identify_date_ranges()

        for ran in ranges:
            try:
                response = requests.get(f'{api_table_a}/{ran[0]}/{ran[1]}')
                self.data.extend(response.json())
            except requests.exceptions.JSONDecodeError:
                print('Given time range exceeds available data.')
                return False
            except Exception as e:
                print(f'An exception occurred during fetching data from API. {e}')
                return False

        return True

    def get_data_single_dates(self) -> bool:
        try:
            first = requests.get(f'{api_table_a}/{self.start}')
            self.data.extend(first.json())

            last = requests.get(f'{api_table_a}/{self.end}')
            self.data.extend(last.json())
        except requests.exceptions.JSONDecodeError:
            print('Given time range exceeds available data.')
            return False
        except Exception as e:
            print(f'An exception occurred during fetching data from API. {e}')
            return False

        return True

    def show_data(self) -> None:
        pprint(self.data)
