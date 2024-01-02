from pathlib import Path

import click

import brain_computer_interface

from .utils import (
    LISTEN_HOST,
    log,
    main,
    module_main_exe,
    SHARED_DIR,
    WEBSERVER_PORT,
)


@main.command()
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=WEBSERVER_PORT)
@click.option('-d', '--data_dir', type=Path, default=SHARED_DIR)
@click.option('-D', '--debug', is_flag=True)
def run_webserver(host, port, data_dir, debug):
    log(brain_computer_interface.run_webserver(host, port, data_dir, debug))


if __name__ == '__main__':
    module_main_exe()
