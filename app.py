import argparse

from model import NBPApp
from ui import ui


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='nbp')
    subparsers = parser.add_subparsers(dest='command')

    show_parser = subparsers.add_parser('show', help='Download data from API and print')
    show_parser.add_argument('-d', '--dates', nargs=2, dest='dates', help='Start and end date in YYYY-MM-DD format separated with space.')
    show_parser.set_defaults(func=NBPApp.show)

    save_parser = subparsers.add_parser('save', help='Save data from API to database')
    save_parser.add_argument('-d', '--dates', nargs=2, dest='dates', help='Start and end date in YYYY-MM-DD format separated with space.')
    save_parser.set_defaults(func=NBPApp.save)

    analyze_parser = subparsers.add_parser('analyze', help='Analyze data from date range')
    analyze_parser.add_argument('-d', '--dates', nargs=2, dest='dates', help='Start and end date in YYYY-MM-DD format separated with space.')
    analyze_parser.set_defaults(func=NBPApp.analyze)

    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('-d', '--dates', nargs='*', dest='dates', help='Start and end date in YYYY-MM-DD format separated with space.')
    report_parser.add_argument('-f', '--format', choices=['csv', 'json'], nargs='+', help='Format: csv and/or json.')
    report_parser.set_defaults(func=NBPApp.report)
    report_range_group = report_parser.add_mutually_exclusive_group()
    report_range_group.add_argument('-c', '--currency', help='Currency code (e.g., USD).')
    report_range_group.add_argument('-ac', '--all-currencies', action='store_true', help='Include all currencies.')
    report_range_group.add_argument('-ah', '--all-historical-data', action='store_true', help='Include all historical data.')

    report_parser = subparsers.add_parser('run', help='Run whole process')
    report_parser.add_argument('-d', '--dates', nargs=2, dest='dates', help='Start and end date in YYYY-MM-DD format separated with space.')
    report_parser.add_argument('-f', '--format', choices=['csv', 'json'], nargs='+', help='Format: csv and/or json.')
    report_parser.set_defaults(func=NBPApp.run)
    report_range_group = report_parser.add_mutually_exclusive_group()
    report_range_group.add_argument('-c', '--currency', help='Currency code (e.g., USD).')
    report_range_group.add_argument('-ac', '--all-currencies', action='store_true', help='Include all currencies.')
    report_range_group.add_argument('-ah', '--all-historical-data', action='store_true', help='Include all historical data.')

    args = parser.parse_args()

    if not args.command:
        ui()
    elif args.command == 'report':
        args.func(args.dates, args.format, args.currency, args.all_currencies, args.all_historical_data)
    elif args.command == 'run':
        args.func(args.dates, args.format, args.currency, args.all_currencies, args.all_historical_data)
    else:
        args.func(args.dates)
