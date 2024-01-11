import click
import json
import pathlib

from . import parse, run_parser
from ..utils import (
    log,
    main,
    module_main_exe,
    DISTRIBUTE_SCHEME,
    SHARED_DIR,
)


@main.command('parse')
@click.argument('name', type=str)
@click.argument('data_path', type=pathlib.Path)
@click.option('-s', '--shared-dir', type=pathlib.Path, default=SHARED_DIR)
def parse_command(name, data_path, shared_dir):
    log(parse(name, json.loads(data_path), shared_dir))


@main.command('run-parser')
@click.argument('name', type=str)
@click.option('-s', '--shared-dir', type=pathlib.Path, default=SHARED_DIR)
@click.option('-d', '--distribute-scheme', type=str, default=DISTRIBUTE_SCHEME)
@click.option('-g', '--group', is_flag=True)
def run_parser_command(name, shared_dir, distribute_scheme, group):
    log(run_parser(name, shared_dir, distribute_scheme, group))


if __name__ == '__main__':
    module_main_exe(__package__)
