import click

from . import upload_mind
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


module_main_exe(__package__)
