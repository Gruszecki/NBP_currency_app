import re
import requests
from pprint import pprint

from consts import api_table_a


class Data:
    @staticmethod
    def validate_date(date: str) -> bool:
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            return True
        return False

    @staticmethod
    def show_data(start_date: str, end_date: str) -> None:
        response = requests.get(f'{api_table_a}/{start_date}/{end_date}')
        pprint(response.json())
