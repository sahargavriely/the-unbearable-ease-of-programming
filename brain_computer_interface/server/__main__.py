import click
import pathlib

from . import run_server
from ..utils import (
    DATA_DIR,
    LISTEN_HOST,
    log,
    main,
    module_main_exe,
    SERVER_PORT,
)


@main.command('run-server')
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
@click.option('-d', '--data_dir', type=pathlib.Path, default=DATA_DIR)
def run_server_command(host, port, data_dir):
    log(run_server(host, port, data_dir))


if __name__ == '__main__':
    module_main_exe('client')
