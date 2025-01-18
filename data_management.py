import re
import requests
from pprint import pprint

from consts import api_table_a


class Data:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start = start_date
        self.end = end_date
        self.data = list[dict]

    def get_data(self) -> None:
        response = requests.get(f'{api_table_a}/{self.start}/{self.end}')
        self.data = response.json()

    def show_data(self) -> None:
        self.get_data()
        pprint(self.data)

    @staticmethod
    def validate_date(date: str) -> bool:
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            return True
        return False
