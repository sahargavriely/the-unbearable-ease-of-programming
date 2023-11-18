from pathlib import Path
import os
import sys
import traceback

import click

import brain_computer_interface

from .utils import (
    DATA_DIR,
    LISTEN_HOST,
    REQUEST_HOST,
    SERVER_PORT,
    WEBSERVER_PORT,
)


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group(context_settings={'show_default': True})
@click.version_option(brain_computer_interface.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('error')
def error_():
    raise RuntimeError('something went terribly wrong :[')


@main.command()
@click.argument('path', type=Path)
def read(path):
    reader = brain_computer_interface.Reader(path)
    gender = 'male' if reader.user_gender == 'm' else 'female' if reader.user_gender == 'f' else 'other'
    print(
        f'User {reader.user_id}: {reader.username},',
        f'born {reader.user_b_day:%B %d, %Y} ({gender})'
    )
    timestamp_format = '%B %d, %Y at %T.%f'
    for snapshot in reader:
        print(
            f'{snapshot.timestamp.strftime(timestamp_format)[:-3]}',
            f'on {snapshot.translation} / {snapshot.rotation}',
            f'with a {snapshot.color_image.width}X{snapshot.color_image.height} color image',
            f'and a {snapshot.depth_image.width}X{snapshot.depth_image.height} depth image'
        )


@main.command()
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
    try:
        main(prog_name='brain_computer_interface')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
