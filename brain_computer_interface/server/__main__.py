import click
import pathlib

from . import run_server_by_scheme
from ..utils import (
    LISTEN_HOST,
    log,
    main,
    module_main_exe,
    PUBLISH_SCHEME,
    SERVER_PORT,
    SHARED_DIR,
)


@main.command('run-server')
@click.option('-ps', '--publish-scheme', type=str, default=PUBLISH_SCHEME)
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
@click.option('-s', '--shared-dir', type=pathlib.Path, default=SHARED_DIR)
def run_server_command(publish_scheme, host, port, shared_dir):
    log(run_server_by_scheme(publish_scheme, host, port, shared_dir))


if __name__ == '__main__':
    module_main_exe('client')
