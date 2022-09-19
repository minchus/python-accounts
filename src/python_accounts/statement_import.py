import datetime
import glob
import logging
import os
from os.path import join, splitext, basename

from python_accounts.banks.natwest import read_csv, insert_to_db


def import_csv(file_path, db_path):
    data = read_csv(file_path)
    logging.info(f"Processing {file_path}")
    insert_to_db(db_path, data)
    logging.info(f"Inserted {len(data)} rows {file_path} into {db_path}.transactions")
    return data


def import_all_csv_in_dir(in_dir, out_dir, db_path):

    file_list = glob.glob(os.path.join(in_dir, '*.csv'))
    if file_list:
        logging.info(f"Found {len(file_list)} files to process in {in_dir}")
    else:
        logging.warning(f"No files to import in {in_dir}")

    for file_path in file_list:
        data = import_csv(file_path, db_path)

        first_date = datetime.datetime.strptime(data[0][0], '%d/%m/%Y').strftime('%Y%m%d')
        last_date = datetime.datetime.strptime(data[-1][0], '%d/%m/%Y').strftime('%Y%m%d')

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        new_file_path = join(out_dir, f"{splitext(basename(file_path))[0]}_{first_date}_{last_date}.csv")
        logging.info(f"Loaded file {file_path} into database, moving to {new_file_path}")
        os.rename(file_path, new_file_path)


