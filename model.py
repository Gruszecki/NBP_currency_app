import re
from pprint import pprint

from api_management import Data
from db import Database


class NBPApp:
    @staticmethod
    def validate_date(func):
        def wrapper(*args, **kwargs):
            for i in range(2):
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', args[i]):
                    print('Wrong data format. At least one provided date does not match pattern YYYY-MM-DD.')
                    return False
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    @validate_date
    def show(start_date: str, end_date: str) -> bool:
        print(f'NBP exchange rates data for date range {start_date} - {end_date}')
        data = Data(start_date, end_date)

        if not data.get_data_in_range():
            return False

        data.show_data()
        return True

    @staticmethod
    @validate_date
    def save(start_date: str, end_date: str) -> bool:
        with Database() as db:
            data = Data(start_date, end_date)
            if data.get_data_in_range():
                return db.save_data(data.data)

    @staticmethod
    @validate_date
    def analyze(start_date: str, end_date: str) -> bool:
        print(f'Analyzing the currencies in provided date range {start_date} - {end_date}')
        data = Data(start_date, end_date)

        if data.get_data_single_dates() and len(data.data) > 1:
            with Database(default_db=False) as temp_db:
                temp_db.save_data(data.data)
                max_diffs = temp_db.get_data_for_analyze(start_date, end_date)

                print(f'Currency with the largest increase {max_diffs[0][2]:.6f} is {max_diffs[0][1]} ({max_diffs[0][0]}).')
                if len(max_diffs) > 1:
                    print(f'Currency with the largest decrease {max_diffs[1][2]:.6f} is {max_diffs[1][1]} ({max_diffs[1][0]}).')
        else:
            print('There is no data for at least one of provided dates.')
            return False
        return True

    @staticmethod
    @validate_date
    def report(start_date: str, end_date: str, report_format: list[str], currency: str = None, all_currencies: bool = False) -> bool:
        with Database() as db:
            data = db.get_all_data()

            for record in data:
                print(record)
