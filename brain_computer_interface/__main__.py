from pathlib import Path

import click

import brain_computer_interface

from .utils import (
    DATA_DIR,
    LISTEN_HOST,
    log,
    main,
    module_main_exe,
    REQUEST_HOST,
    SERVER_PORT,
    WEBSERVER_PORT,
)


@main.command()
@click.argument('path', type=str)
def read(path):
    reader = brain_computer_interface.Reader(path)
    print(reader.user)
    for snapshot in reader:
        print(snapshot)


@main.group()
def client():
    pass


@client.command()
@click.argument('path', type=str)
@click.option('-h', '--host', type=str, default=REQUEST_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
def upload_mind(host, port, path):
    log(brain_computer_interface.upload_mind(path, host, port))


@client.command()
@click.argument('user_id', type=int)
@click.argument('thought', type=str)
@click.option('-h', '--host', type=str, default=REQUEST_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
def upload_thought(host, port, user_id, thought):
    log(brain_computer_interface.upload_thought(user_id, thought, host, port))


@main.command()
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
@click.option('-d', '--data_dir', type=Path, default=DATA_DIR)
def run_server(host, port, data_dir):
    log(brain_computer_interface.run_server(host, port, data_dir))


@main.command()
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=WEBSERVER_PORT)
@click.option('-d', '--data_dir', type=Path, default=DATA_DIR)
@click.option('-D', '--debug', is_flag=True)
def run_webserver(host, port, data_dir, debug):
    log(brain_computer_interface.run_webserver(host, port, data_dir, debug))


if __name__ == '__main__':
    module_main_exe()
