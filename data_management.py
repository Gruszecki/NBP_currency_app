import requests
from pprint import pprint

from consts import api_table_a
from utils import identify_date_ranges, calculate_working_dates


class Data:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start = start_date
        self.end = end_date
        self.data = []

    def get_data_in_range(self) -> bool:
        ranges = identify_date_ranges(self.start, self.end)

        for r in ranges:
            start, end = calculate_working_dates(r[0], r[1])
            try:
                response = requests.get(f'{api_table_a}/{start}/{end}')
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
