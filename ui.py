import re

from model import NBPApp
from utils import validate_date


def ui():
    print('Please provide the first and the last date from rang you want to work with in YYYY-MM-DD format.')
    first_date = input('First date: ')
    if not validate_date(first_date):
        return

    last_date = input('Last date: ')
    if not validate_date(last_date):
        return

    app = NBPApp()

    response = input('Do you want to show data from NBP? [y/n] ')
    if response.lower() == 'y':
        app.show(first_date, last_date)

    response = input('Do you want to save data in local database? [y/n] ')
    if response.lower() == 'y':
        app.save(first_date, last_date)

    response = input('Do you want to analyze data? [y/n] ')
    if response.lower() == 'y':
        app.analyze(first_date, last_date)

    response = input('Do you want to create report(s)? [y/n] ')
    if response.lower() == 'y':
        f = input('Choose file format(s) from those available, separated by space [json|csv] ')

        response = input('Do you want to analyze all currencies? [y/n] ')
        all_currencies = True if response.lower() == 'y' else False

        code = None
        if not all:
            code = input('Type currency code for analyze (e.g. EUR): ')

        app.report(start_date=first_date, end_date=last_date, report_format=f.strip().split(' '), all_currencies=all_currencies, currency=code)
