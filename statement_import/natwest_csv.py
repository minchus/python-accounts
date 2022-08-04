#!/usr/bin/env python

import csv
import datetime
import sqlite3


def read_csv(file_path):
    # Remove blank lines and strip trailing comma
    lines = filter(None, (line.rstrip().rstrip(",") for line in open(file_path)))

    header = next(lines)
    if header != "Date, Type, Description, Value, Balance, Account Name, Account Number":
        raise Exception(f"{file_path} did not contain the expected column headers")

    reader = csv.reader(lines, quotechar='"')
    data = []

    def lstrip_quote(s):
        return s.lstrip("'")  # Strip leading quote used as a text qualifier

    for row in reader:
        data.append(tuple(map(lstrip_quote, row)))

    return data


def insert_to_db(db_path, data):

    data_to_insert = []
    for row in data:
        # Convert date format to SQLite format
        new_row = (datetime.datetime.strptime(row[0], '%d/%m/%Y').strftime('%Y-%m-%d'), ) + row[1:]
        data_to_insert.append(new_row)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany("REPLACE INTO transactions"
                  "('date', 'type', 'description', 'value', 'balance', 'account_name', 'account_number')"
                  "VALUES (?,?,?,?,?,?,?)", data_to_insert)
    conn.commit()
    conn.close()

    return



