from model import NBPApp
from utils import validate_dates


def ui():
    print('Please provide the first and the last date from rang you want to work with in YYYY-MM-DD format.')
    first_date = input('First date: ')
    if not validate_dates([first_date]):
        return

    last_date = input('Last date: ')
    if not validate_dates([last_date]):
        return

    dates = [first_date, last_date]

    app = NBPApp()

    response = input('Do you want to show data from NBP? [y/n] ')
    if response.lower() == 'y':
        app.show(dates)

    response = input('Do you want to save data in local database? [y/n] ')
    if response.lower() == 'y':
        app.save(dates)

    response = input('Do you want to analyze data? [y/n] ')
    if response.lower() == 'y':
        app.analyze(dates)

    response = input('Do you want to create report(s)? [y/n] ')
    if response.lower() == 'y':
        f = input('Choose file format(s) from those available, separated by space [json|csv] ')

        response = input('Do you want to analyze all historical data? [y/n] ')
        all_data = True if response.lower() == 'y' else False

        all_currencies = None
        code = None

        if not all_data:
            response = input('Do you want to analyze all currencies? [y/n] ')
            all_currencies = True if response.lower() == 'y' else False

            if not all_currencies:
                code = input('Type currency code for analyze (e.g. EUR): ')

        app.report(dates=dates, report_format=f.strip().split(' '), all_currencies=all_currencies, all_data=all_data, currency=code)
