from pprint import pprint

import utils
from data_management import Data
from db import Database
from save_management import Csv, Json
from utils import calculate_working_dates, validate_dates, validate_dates_argument


class NBPApp:
    @staticmethod
    def _print_data(data):
        pprint(data.data)

    @staticmethod
    def _save_to_db(data: Data) -> bool:
        with Database() as db:
            return db.save_data(data.data)

    @staticmethod
    @validate_dates_argument
    def show(dates: list[str]) -> bool:
        print(f'NBP exchange rates data for date range {dates[0]} - {dates[1]}')
        data = Data(dates[0], dates[1])

        if not data.get_data_in_range():
            return False

        data.show_data()
        return True

    @staticmethod
    @validate_dates_argument
    def save(dates: list[str]) -> bool:
        data = Data(dates[0], dates[1])
        if data.get_data_in_range():
            return NBPApp._save_to_db(data)

    @staticmethod
    @validate_dates_argument
    def analyze(dates: list[str], validate_range=True) -> bool:
        start_date, end_date = dates

        if validate_range:
            start_date, end_date = utils.calculate_working_dates(dates)

        print(f'Analyzing the currencies in date range {start_date} - {end_date}')

        if start_date == end_date:
            print('Cannot perform analysis because the first and the last date are the same.')
            return False

        with Database() as db:
            result = db.get_data_for_max_diffs(start_date, end_date)

            if result:
                max_inc, max_dec = result

                print(f'Currency with the largest increase is {max_inc[1]} ({max_inc[0]}) and it changed by '
                      f'{max_inc[4]:.6f} from {max_inc[2]} to {max_inc[3]} which is {max_inc[5]}%.')
                print(f'Currency with the largest decrease is {max_dec[1]} ({max_dec[0]}) and it changed by '
                      f'{max_dec[4]:.6f} from {max_dec[2]} to {max_dec[3]} which is {max_dec[5]}%.')
            else:
                print('Analyze could not be performed.')
                return False

            return True

    @staticmethod
    def report(dates: list[str], report_format: list[str], currency: str = None,
               all_currencies: bool = False, all_data: bool = False, validate_range: bool = True) -> bool:
        if dates:
            start_date, end_date = dates

        if not all_data:
            if len(dates) < 2:
                print('Start date and end date must be provided.')
                return False
            if not validate_dates(dates):
                print('At least one provided data has wrong format.')
                return False

            if validate_range:
                start_date, end_date = utils.calculate_working_dates(dates)
        else:
            with Database() as db:
                start_date, end_date = db.get_db_range()[0]

        with Database() as db:
            if currency:
                data = db.get_data_for_currency_diff(currency.upper(), start_date, end_date)
            else:
                data = db.get_data_for_all_diff(start_date, end_date)

        if data and all(data[0]):
            if 'json' in report_format:
                save_format = Json()
                save_format.save(data)
            if 'csv' in report_format:
                save_format = Csv()
                save_format.save(data)

            print('Report(s) generated.')
        else:
            print('Not all requested data are available in database.')
            return False

        return True

    @staticmethod
    def run(dates: list[str], report_format: list[str], currency: str = None,
            all_currencies: bool = False, all_data: bool = False) -> bool:
        start_date, end_date = calculate_working_dates(dates)
        data = Data(start_date, end_date)

        if not data.get_data_in_range():
            print('Something went wrong')
            return False

        NBPApp._print_data(data=data)
        print(f'Working date range: {start_date} - {end_date}')
        save_res = NBPApp._save_to_db(data=data)

        if save_res:
            NBPApp.analyze([start_date, end_date], validate_range=False)
            NBPApp.report(dates=[start_date, end_date], report_format=report_format, currency=currency,
                          all_currencies=all_currencies, all_data=all_data, validate_range=False)
        else:
            print('An error while saving data in database occurred.')
            return False

        return True
