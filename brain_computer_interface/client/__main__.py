import click

from . import (
    upload_mind,
    upload_thought,
)
from .reader import Reader
from ..utils import (
    log,
    main,
    module_main_exe,
    REQUEST_HOST,
    SERVER_PORT,
)


@main.command()
@click.argument('path', type=str)
def read(path):
    reader = Reader(path)
    print(reader.user)
    for snapshot in reader:
        print(snapshot)


@main.command('upload-mind')
@click.argument('path', type=str)
@click.option('-h', '--host', type=str, default=REQUEST_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
def upload_mind_command(host, port, path):
    log(upload_mind(path, host, port))


@main.command('upload-thought')
@click.argument('user_id', type=int)
@click.argument('thought', type=str)
@click.option('-h', '--host', type=str, default=REQUEST_HOST)
@click.option('-p', '--port', type=int, default=SERVER_PORT)
def upload_thought_command(host, port, user_id, thought):
    log(upload_thought(user_id, thought, host, port))


if __name__ == '__main__':
    module_main_exe(__package__)
