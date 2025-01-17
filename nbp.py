import argparse

from data import Data



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--start_date', help='Start date in YYYY-MM-DD format, e.g. 2025-01-17')
    parser.add_argument('-ed', '--end_date', help='End date in YYYY-MM-DD format, e.g. 2025-01-17')
    parser.add_argument('-s', '--save', help='Save data to database. Must be used with -sd and -ed arguments', action='store_true')
    parser.add_argument('-a', '--analyze', help='Determine the currencies with the greatest increase and decrease in exchange rate. Must be used with -sd and -ed arguments', action='store_true')
    parser.add_argument('-r', '--report', help='Generate report. Must be used with --csv or/and --json flag(s). Must be used with -c argument or --all flag', action='store_true')
    parser.add_argument('--csv', help='Save report in csv format', action='store_true')
    parser.add_argument('--json', help='Save report in json format', action='store_true')
    parser.add_argument('-c', '--currency', help='Currency in currency code format (e.g. PLN) to be analyzed over time (to be saved in report)')
    parser.add_argument('--all', help='Analyze all historic data over time (to be saved in report)', action='store_true')

    args = parser.parse_args()

    if args.start_date and args.end_date:
        if not args.analyze and not args.report:
            if Data.validate_date(args.start_date) and Data.validate_date(args.end_date):
                Data.show_data(args.start_date, args.end_date)
            else:
                print('Wrong data format. At least one provided date does not match pattern YYYY-MM-DD.\n')
        else:
            if args.analyze:
                pass
            if args.report:
                pass
