from pprint import pprint

from data_management import Data
from db import Database
from save_management import Csv, Json
from utils import calculate_working_dates, validate_date


class NBPApp:
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
    def print_data(data):
        pprint(data.data)

    @staticmethod
    def save(data: Data) -> bool:
        with Database() as db:
            return db.save_data(data.data)

    @staticmethod
    @validate_date
    def analyze(start_date: str, end_date: str) -> bool:
        print(f'Analyzing the currencies in provided date range {start_date} - {end_date}')
        with Database() as db:
            max_inc, max_dec = db.get_data_for_max_diffs(start_date, end_date)

            print(f'Currency with the largest increase is {max_inc[1]} ({max_inc[0]}) and it changed by '
                  f'{max_inc[4]:.6f} from {max_inc[2]} to {max_inc[3]} which is {max_inc[5]}%.')
            print(f'Currency with the largest decrease is {max_dec[1]} ({max_dec[0]}) and it changed by '
                  f'{max_dec[4]:.6f} from {max_dec[2]} to {max_dec[3]} which is {max_dec[5]}%.')

        return True

    @staticmethod
    @validate_date
    def report(start_date: str, end_date: str, report_format: list[str], currency: str = None, all_currencies: bool = False) -> bool:
        with Database() as db:
            if currency:
                data = db.get_data_for_currency_diff(currency.upper(), start_date, end_date)
            elif all_currencies:
                data = db.get_data_for_all_diff(start_date, end_date)

            if 'json' in report_format:
                save_format = Json()
                save_format.save(data)
            if 'csv' in report_format:
                save_format = Csv()
                save_format.save(data)

    @staticmethod
    def run(start_date: str, end_date: str, report_format: list[str], currency: str = None, all_currencies: bool = False) -> bool:
        data = Data(start_date, end_date)

        start_date, end_date = calculate_working_dates(start_date, end_date)

        if not data.get_data_in_range():
            print('Something went wrong')
            return False

        NBPApp.print_data(data=data)
        print(f'Working date range: {start_date} - {end_date}')
        save_res = NBPApp.save(data=data)

        if save_res:
            NBPApp.analyze(start_date=start_date, end_date=end_date)
            NBPApp.report(start_date, end_date, report_format, currency, all_currencies)
        else:
            print('An error while saving data in database occurred.')
            return False
