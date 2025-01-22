import urllib.error
import urllib.request
from pprint import pprint
import json

from consts import api_table_a
from utils import identify_date_ranges, calculate_working_dates


class Data:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start = start_date
        self.end = end_date
        self.data = []

    @staticmethod
    def _api_call(url: str) -> dict | None:
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read().decode("utf-8")
            return json.loads(data)
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_data_in_range(self) -> bool:
        ranges = identify_date_ranges(self.start, self.end)

        for r in ranges:
            start, end = calculate_working_dates(r[0], r[1])
            response = self._api_call(f'{api_table_a}/{start}/{end}')
            if response:
                self.data.extend(response)
            else:
                return False

        return True

    def check_dates_availability(self) -> bool:
        first = self._api_call(f'{api_table_a}/{self.start}')
        last = self._api_call(f'{api_table_a}/{self.end}')

        print(first, last)

        return True

    def show_data(self) -> None:
        pprint(self.data)
