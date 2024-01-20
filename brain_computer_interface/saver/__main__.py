import click
import json
import pathlib

from . import Saver
from ..utils import (
    DATABASE,
    DISTRIBUTE_SCHEME,
    log,
    main,
    module_main_exe,
)


@main.group()
def save():
    pass


@save.command()
@click.argument('user-id', type=int)
@click.argument('datetime', type=int)
@click.argument('topic', type=str)
@click.argument('path', type=pathlib.Path)
@click.option('-d', '--database', type=str, default=DATABASE)
def snapshot(user_id, datetime, topic, path, database):
    with path.open('r') as file:
        data = json.load(file)
    log(Saver(database).save_snapshot_topic(user_id, datetime, topic, data))


@save.command()
@click.argument('user-id', type=int)
@click.argument('path', type=pathlib.Path)
@click.option('-d', '--database', type=str, default=DATABASE)
def user(user_id, path, database):
    with path.open('r') as file:
        data = json.load(file)
    log(Saver(database).save_user(user_id, data))


@main.command('run-saver')
@click.option('-d', '--database', type=str, default=DATABASE)
@click.option('-ds', '--distribute-scheme', type=str,
              default=DISTRIBUTE_SCHEME)
def run_saver(database, distribute_scheme):
    log(Saver.run(database, distribute_scheme))


if __name__ == '__main__':
    module_main_exe(__package__)
