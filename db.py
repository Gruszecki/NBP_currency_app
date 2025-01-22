import sqlite3

from consts import database_name


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS exchange_rates (
                        date DATE NOT NULL, 
                        code TEXT NOT NULL,
                        mid REAL NOT NULL,
                        PRIMARY KEY (date, code)
                        )''')

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS currencies_codes (
                        code DATE NOT NULL PRIMARY KEY, 
                        currency TEXT NOT NULL
                        )''')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'An error occurred while operating with database. {exc_val}.')
            self.conn.rollback()

        self.conn.close()

        return True

    def save_data(self, data: list[dict]) -> bool:
        for record in data:
            record_date = record['effectiveDate']
            for rate in record['rates']:
                self.cursor.execute('INSERT OR IGNORE INTO exchange_rates (date, code, mid) VALUES (?, ?, ?)',
                                    (record_date, rate['code'], round(rate['mid'], 6)))

                self.cursor.execute('INSERT OR IGNORE INTO currencies_codes (code, currency) VALUES (?, ?)',
                                    (rate['code'], rate['currency']))
        try:
            self.conn.commit()
            print('Data saved in database properly.')
        except Exception as e:
            print(f'An exception occurred during saving data to database. {e}')
            return False

        return True

    def get_data_for_currency_diff(self, code: str, first: str, last: str) -> list:
        self.cursor.execute('WITH first as (SELECT date, code, mid FROM exchange_rates WHERE code IS ? AND date is ?), '
                            'last as (SELECT date, code, mid FROM exchange_rates WHERE code IS ? AND date is ?)'
                            'SELECT first.code, first.date, last.date, first.mid, last.mid, '
                            'ROUND(last.mid-first.mid, 6), ROUND((last.mid*100/first.mid)-100, 3) '
                            'FROM first FULL JOIN last ON first.code = last.code',
                            (code, first, code, last))
        return self.cursor.fetchall()

    def get_data_for_all_diff(self, first: str, last: str) -> list:
        self.cursor.execute('WITH first as (SELECT date, code, mid FROM exchange_rates WHERE date is ?), '
                            'last as (SELECT date, code, mid FROM exchange_rates WHERE date is ?) '
                            'SELECT first.code, first.date, last.date, first.mid, last.mid, '
                            'ROUND(last.mid-first.mid, 6), ROUND((last.mid*100/first.mid)-100, 3) '
                            'FROM first FULL JOIN last ON first.code = last.code',
                            (first, last))
        return self.cursor.fetchall()

    def get_data_for_max_diffs(self, first: str, last: str) -> list:
        self.cursor.execute(
            'WITH diffs AS '
            '(WITH first AS (SELECT code, mid FROM exchange_rates WHERE date is ?), '
            'last AS (SELECT code, mid FROM exchange_rates WHERE date is ?) '
            'SELECT first.code, first.mid as first_mid, last.mid AS last_mid, last.mid-first.mid AS diff, ROUND((last.mid*100/first.mid)-100, 3) AS change '
            'FROM first INNER JOIN last ON first.code = last.code) '
            'SELECT diffs.code, currency, first_mid, last_mid, diff, change '
            'FROM diffs LEFT JOIN currencies_codes ON diffs.code = currencies_codes.code '
            'WHERE change = (SELECT MAX(change) FROM diffs) OR change = (SELECT MIN(change) FROM diffs) '
            'ORDER BY change DESC',
            (first, last)
        )

        return self.cursor.fetchall()

    def get_all_data(self):
        self.cursor.execute('SELECT * FROM exchange_rates')
        return self.cursor.fetchall()
