import os
import sqlite3
from pprint import pprint

from consts import database_name


class Database:
    def __init__(self, default_db: bool = True):
        self.default_db = default_db
        db_name = database_name if self.default_db else 'temp.db'

        self.conn = sqlite3.connect(f'{db_name}')
        self.cursor = self.conn.cursor()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS exchange_rates (
                        date DATE NOT NULL, 
                        code TEXT NOT NULL, 
                        currency TEXT NOT NULL, 
                        mid REAL NOT NULL,
                        PRIMARY KEY (date, code)
                        )''')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'An error occurred while writing to the database. {exc_val}.')
            self.conn.rollback()

        self.conn.close()

        if not self.default_db:
            os.remove('temp.db')

        return True

    def save_data(self, data: list[dict]) -> bool:
        for record in data:
            record_date = record['effectiveDate']
            for rate in record['rates']:
                self.cursor.execute('INSERT OR IGNORE INTO exchange_rates (date, code, currency, mid) VALUES (?, ?, ?, ?)',
                                    (record_date, rate['code'], rate['currency'], round(rate['mid'], 6)))
        try:
            self.conn.commit()
        except Exception as e:
            print(f'An exception occurred during saving data to database. {e}')
            return False

        return True

    def get_data_for_date(self, date: str) -> list:
        self.cursor.execute('SELECT * FROM exchange_rates WHERE date is ?', (date,))
        return self.cursor.fetchall()

    def get_data_for_analyze(self, first: str, last: str) -> list:
        self.cursor.execute(
            'WITH diffs AS '
            '(WITH first AS (SELECT code, currency, mid FROM exchange_rates WHERE date is ?),'
            'last AS (SELECT code, currency, mid FROM exchange_rates WHERE date is ?)'
            'SELECT first.code, first.currency, last.mid-first.mid AS change '
            'FROM first INNER JOIN last ON first.code = last.code)'
            'SELECT code, currency, change FROM diffs '
            'WHERE change = (SELECT MAX(change) FROM diffs) OR change = (SELECT MIN(change) FROM diffs)'
            'ORDER BY change DESC',
            (first, last)
        )

        return self.cursor.fetchall()

    def read_db(self):
        self.cursor.execute('SELECT * FROM exchange_rates')
        pprint(self.cursor.fetchall())

    def get_all_data(self):
        self.cursor.execute('SELECT date, code, mid FROM exchange_rates')
        return self.cursor.fetchall()
