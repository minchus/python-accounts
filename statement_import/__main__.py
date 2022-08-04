import argparse
import datetime
import glob
import logging
import os

from os.path import basename, join, splitext
from statement_import.natwest_csv import insert_to_db, read_csv


def import_csv(file_path, db_path):
    data = read_csv(file_path)
    logging.info(f"Loading {len(data)} rows from {file_path} into {db_path}.transactions")
    insert_to_db(db_path, data)
    return data


def import_all_csv_in_dir(dir_path, db_path):

    file_list = glob.glob(os.path.join(dir_path, '*.csv'))
    if file_list:
        logging.info(f"Loading {len(file_list)} files into {db_path}.transactions")
    else:
        logging.warning(f"No files to import in {dir_path}")

    for file_path in file_list:
        data = import_csv(file_path, db_path)

        first_date = datetime.datetime.strptime(data[0][0], '%d/%m/%Y').strftime('%Y%m%d')
        last_date = datetime.datetime.strptime(data[-1][0], '%d/%m/%Y').strftime('%Y%m%d')

        output_dir = join(dir_path, "processed")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        new_file_path = join(output_dir, f"{splitext(basename(file_path))[0]}_{first_date}_{last_date}.csv")
        logging.info(f"Loaded file {file_path} into database, moving to {new_file_path}")
        os.rename(file_path, new_file_path)


logging.basicConfig(
    level=os.environ.get('LOGLEVEL', 'WARNING').upper(),
    format="%(asctime)s [%(levelname)s] %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Path to csv file to import')
parser.add_argument('-d', '--dir', help='Import directory', default="data/import")
parser.add_argument('-t', '--test', action="store_true", help='Test mode')
args = parser.parse_args()

if args.test:
    logging.warning("Running in test mode")
    DATA_DIR = r"E:\Dropbox\Accounts\python-accounts\data"
else:
    DATA_DIR = r"E:\Dropbox\Accounts\python-accounts\data_test"

DB_PATH = join(DATA_DIR, "mchung_accounts.db")
IMPORT_DIR = join(DATA_DIR, "import")
logging.info(f"DB_PATH: {DB_PATH}")
logging.info(f"IMPORT_DIR: {IMPORT_DIR}")

if args.file:
    import_csv(args.file, DB_PATH)
else:
    import_all_csv_in_dir(IMPORT_DIR, DB_PATH)
