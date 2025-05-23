import click
import pathlib

from . import run_server_by_scheme
from ..utils import (
    LISTEN_HOST,
    log,
    main,
    module_main_exe,
    DISTRIBUTE_SCHEME,
    SERVER_PORT,
    SHARED_DIR,
)


@main.command('run-server')
@click.option('-d', '--distribute-scheme', type=str, default=DISTRIBUTE_SCHEME)
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
@click.option('-s', '--shared-dir', type=pathlib.Path, default=SHARED_DIR)
def run_server_command(distribute_scheme, host, port, shared_dir):
    log(run_server_by_scheme(distribute_scheme, host, port, shared_dir))


module_main_exe(__package__)
