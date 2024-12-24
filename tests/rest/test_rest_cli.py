import ast
import re
import subprocess

import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys


def test_error_format(client, conf, user):
    with pytest.raises(RuntimeError,
                       match=re.escape(
                           f'ERROR: GET request to http:/'
                           f'/{conf.REQUEST_HOST}:{conf.REST_SERVER_PORT}/'
                           f'/users/{user.id} failed (400): '
                           f'User id {user.id} does not exists')):
        _get_command(conf, 'user', user.id)


def test_user(client, conf, database, user):
    database.save_user(user.id, user.jsonify())
    assert _get_command(conf, 'users') == [user.id]
    assert _get_command(conf, 'user', user.id) == user.jsonify()


def test_snapshot(client, conf, database, user, parsed_data,
                  snapshot):
    datetime = snapshot.datetime
    for topic in CONFIG_OPTIONS:
        database.save_snapshot_topic(
            user.id, datetime, topic, parsed_data[topic][keys.data])
    assert _get_command(conf, 'user-snapshots', user.id) == [datetime]
    saved_snap = dict(datetime=datetime)
    for topic in CONFIG_OPTIONS:
        saved_snap[topic] = parsed_data[topic][keys.data]
        assert saved_snap[topic] == \
            _get_command(conf, 'user-snapshot-topic', user.id, datetime, topic)
    assert saved_snap == \
        _get_command(conf, 'user-snapshot', user.id, datetime)

    _get_command(conf, 'user-snapshot-topic-data', user.id, datetime,
                 keys.color_image)
    _get_command(conf, 'user-snapshot-topic-data', user.id, datetime,
                 keys.depth_image)


###############################################################################
# UTILS


def _get_command(conf, *args):
    cmd = ['python', '-m', 'brain_computer_interface.rest', 'get',
           '-h', conf.REQUEST_HOST, '-p', str(conf.REST_SERVER_PORT),
           *[str(arg) for arg in args]]
    try:
        pro = subprocess.run(cmd, capture_output=True, check=True, timeout=5)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stdout.decode().strip())
    ret = pro.stdout.decode().strip()
    try:
        return ast.literal_eval(ret)
    except Exception:
        return ret
