import json
from abc import ABC, abstractmethod
from collections import defaultdict
from pprint import pprint


class Format(ABC):
    @abstractmethod
    def save(self, data: list):
        """Accepts list of tuples in following format: (date, code, mid)"""
        pass


class Json(Format):
    def save(self, data: list[tuple]):
        report_data = defaultdict(dict)

        if len(data) == 1:
            filename = f'analyze_{data[0][1]}_-_{data[0][2]}_{data[0][0]}.json'
        else:
            filename = f'analyze_{data[0][1]}_-_{data[0][2]}_all.json'

        for first_date, last_date, code, first_mid, last_mid, diff, change_per in data:
            report_data[code].update({'first_date': first_date})
            report_data[code].update({'last_date': last_date})
            report_data[code].update({'first_mid': first_mid})
            report_data[code].update({'last_mid': last_mid})
            report_data[code].update({'diff': diff})
            report_data[code].update({'diff_percentage': change_per})

        report_data_json = json.dumps(report_data, ensure_ascii=False, indent=4)

        with open(filename, 'w') as f:
            f.write(report_data_json)


class Csv(Format):
    def save(self, data: list[tuple]):
        if len(data) == 1:
            filename = f'analyze_{data[0][1]}_-_{data[0][2]}_{data[0][0]}.csv'
        else:
            filename = f'analyze_{data[0][1]}_-_{data[0][2]}_all.csv'

        with open(filename, 'w') as f:
            f.write('code;first date;last date;first mid;last mid;diff;diff percentage\n')

            for record in data:
                for col in record:
                    f.write(f'{col};')
                f.write('\n')
