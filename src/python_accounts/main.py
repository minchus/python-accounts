import click
import logging
import os

from configparser import ConfigParser
from python_accounts.statement_import import import_all_csv_in_dir, import_csv


DEFAULT_CFG = 'config/default.ini'


def configure(ctx, param, filename):
    cfg = ConfigParser()
    cfg.read(filename)
    try:
        options = dict(cfg['options'])
    except KeyError:
        options = {}
    ctx.default_map = options


@click.command()
@click.option(
    '-c', '--config',
    type=click.Path(dir_okay=False),
    default=DEFAULT_CFG,
    callback=configure,
    is_eager=True,
    expose_value=False,
    help='Read option defaults from the specified INI file',
    show_default=True,
)
@click.option("--file", "-f", type=click.Path(dir_okay=False))
@click.option("--in-dir", "-i", type=click.Path(dir_okay=True), required=True, help='Input directory')
@click.option("--out-dir", "-o", type=click.Path(dir_okay=True), required=True, help='Directory for processed files')
@click.option("--db-path", "-d", type=click.Path(dir_okay=False), required=True, help='Path to sqlite DB file')
def main(file, in_dir, out_dir, db_path):
    logging.basicConfig(
        level=os.environ.get('LOGLEVEL', 'INFO').upper(),
        format="%(asctime)s [%(levelname)s] %(message)s")

    logging.info(f"{in_dir=}")
    logging.info(f"{out_dir=}")
    logging.info(f"{db_path=}")

    if file:
        import_csv(file, db_path)
    else:
        import_all_csv_in_dir(in_dir, out_dir, db_path)
