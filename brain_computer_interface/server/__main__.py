import click
import pathlib

from . import run_server_by_scheme
from ..utils import (
    DATA_DIR,
    LISTEN_HOST,
    log,
    main,
    module_main_exe,
    PUBLISH_SCHEME,
    SERVER_PORT,
)


@main.command('run-server')
@click.option('-ps', '--publish-scheme', type=str, default=PUBLISH_SCHEME)
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
@click.option('-d', '--data-dir', type=pathlib.Path, default=DATA_DIR)
def run_server_command(publish_scheme, host, port, data_dir):
    log(run_server_by_scheme(publish_scheme, host, port, data_dir))


if __name__ == '__main__':
    module_main_exe('client')
