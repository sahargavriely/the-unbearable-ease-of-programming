import json
import click

import requests

from . import run_rest_server
from ..utils import (
    DATABASE_SCHEME,
    LISTEN_HOST,
    keys,
    log,
    main,
    module_main_exe,
    REST_SERVER_PORT,
    REQUEST_HOST,
)


_base_url = ''


def _check_response(response):
    if response.ok:
        return
    error = response.json()[keys.error]
    raise RuntimeError(f'{response.request.method} request to '
                       f'{response.request.url} failed '
                       f'({response.status_code}): {error}')


def _request(url, **data):
    url = f'{_base_url}/{url}'
    response = requests.get(url, params=data)
    _check_response(response)
    try:
        to_show = response.json()
    except json.decoder.JSONDecodeError:
        to_show = response.text
    log(to_show)


###############################################################################


@main.command('run-rest-server')
@click.option('-h', '--host', type=str, default=LISTEN_HOST)
@click.option('-p', '--port', type=int, default=REST_SERVER_PORT)
@click.option('-d', '--database-scheme', type=str, default=DATABASE_SCHEME)
def run_rest_server_command(host, port, database_scheme):
    log(run_rest_server(host, port, database_scheme))


@main.group()
@click.option('-h', '--host', default=REQUEST_HOST)
@click.option('-p', '--port', default=REST_SERVER_PORT)
def get(host, port):
    global _base_url
    _base_url = f'http://{host}:{port}/'


@get.command
def users():
    _request('users')


@get.command
@click.argument('id', type=int)
def user(id):
    _request(f'users/{id}')


@get.command
@click.argument('id', type=int)
def user_snapshots(id):
    _request(f'users/{id}/snapshots')


@get.command
@click.argument('id', type=int)
@click.argument('datetime', type=int)
def user_snapshot(id, datetime):
    _request(f'users/{id}/snapshots/{datetime}')


@get.command
@click.argument('id', type=int)
@click.argument('datetime', type=int)
@click.argument('topic', type=str)
def user_snapshot_topic(id, datetime, topic):
    _request(f'users/{id}/snapshots/{datetime}/{topic}')


@get.command
@click.argument('id', type=int)
@click.argument('datetime', type=int)
@click.argument('topic', type=str)
def user_snapshot_topic_data(id, datetime, topic):
    _request(f'/users/{id}/snapshots/{datetime}/{topic}/data')


if __name__ == '__main__':
    module_main_exe(__package__)
