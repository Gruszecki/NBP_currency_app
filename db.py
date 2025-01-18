import sqlite3

from data_management import Data


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('nbp_exchange_rates.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS exchange_rates (
                        date DATE NOT NULL, 
                        code TEXT NOT NULL, 
                        currency TEXT NOT NULL, 
                        mid INTEGER NOT NULL,
                        PRIMARY KEY (date, code)
                        )''')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'An error occurred while writing to the database. {exc_val}.')
            self.conn.rollback()

        self.conn.close()

        return True

    def save_data(self, records: Data) -> None:
        for record in records.data:
            record_date = record['effectiveDate']
            for rate in record['rates']:
                self.cursor.execute('INSERT OR IGNORE INTO exchange_rates (date, code, currency, mid) VALUES (?, ?, ?,?)',
                                    (record_date, rate['code'], rate['currency'], rate['mid']))
        self.conn.commit()

    def read_data(self) -> None:
        self.cursor.execute('SELECT * FROM exchange_rates ORDER BY date, code')
        for row in self.cursor.fetchall():
            print(row)
