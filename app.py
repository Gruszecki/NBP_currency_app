import argparse

from model import NBPApp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='nbp')
    subparsers = parser.add_subparsers(dest='command')

    dates_template = {
        'dest': 'dates',
        'nargs': 2,
        'help': 'Start and end date in YYYY-MM-DD format.',
    }

    show_parser = subparsers.add_parser('show', help='Download data from API and print')
    show_parser.add_argument(**dates_template)
    show_parser.set_defaults(func=NBPApp.show)

    save_parser = subparsers.add_parser('save', help='Save data from API to database')
    save_parser.add_argument(**dates_template)
    save_parser.set_defaults(func=NBPApp.save)

    analyze_parser = subparsers.add_parser('analyze', help='Analyze data from date range')
    analyze_parser.add_argument(**dates_template)
    analyze_parser.set_defaults(func=NBPApp.analyze)

    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument(**dates_template)
    report_parser.add_argument('-f', '--format', choices=['csv', 'json'], nargs='+', help='Format: csv and/or json.')
    report_parser.set_defaults(func=NBPApp.report)
    report_range_group = report_parser.add_mutually_exclusive_group()
    report_range_group.add_argument('-c', '--currency', help='Currency code (e.g., USD).')
    report_range_group.add_argument('--all', action='store_true', help='Include all currencies.')

    report_parser = subparsers.add_parser('run', help='Generate report')
    report_parser.add_argument(**dates_template)
    report_parser.add_argument('-f', '--format', choices=['csv', 'json'], nargs='+', help='Format: csv and/or json.')
    report_parser.set_defaults(func=NBPApp.run)
    report_range_group = report_parser.add_mutually_exclusive_group()
    report_range_group.add_argument('-c', '--currency', help='Currency code (e.g., USD).')
    report_range_group.add_argument('--all', action='store_true', help='Include all currencies.')

    args = parser.parse_args()

    if not args.command:
        print('Show UI')
    elif args.command == 'report' or args.command == 'run':
        args.func(*args.dates, args.format, args.currency, args.all)
    else:
        args.func(*args.dates)
