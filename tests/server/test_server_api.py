import json
import socket
import time

import pytest

from brain_computer_interface.protocol import Snapshot
from brain_computer_interface.server import run_server_by_scheme
from utils import (
    mock_upload_mind,
    mock_upload_thought,
    _get_path,
    _serialize_thought,
)


def test_run_server(conf, server, server_publish_dir, user, snapshot):
    if server_publish_dir.exists():
        assert not [p for p in server_publish_dir.iterdir()]
    mock_upload_mind(conf, user, snapshot)
    publish_data_file = server_publish_dir / 'data.json'
    assert publish_data_file.exists()
    assert publish_data_file.is_file()
    with publish_data_file.open('r') as file:
        data = json.load(file)
    user_json = data['user']
    snapshot_json = data['snapshot']
    assert user.jsonify() == user_json
    assert repr(snapshot) == repr(Snapshot.from_json(snapshot_json))
    assert snapshot.color_image.data == Snapshot.from_json(
        snapshot_json).color_image.data
    assert snapshot.depth_image.data == Snapshot.from_json(
        snapshot_json).depth_image.data


def test_run_server_by_scheme_error():
    bad_scheme = 'sike'
    url = f'{bad_scheme}:///nowhere'
    error_msg = f'Publish scheme {bad_scheme!r} is not supported'
    with pytest.raises(ValueError, match=error_msg):
        run_server_by_scheme(url)


def test_thought(conf, server):
    thought_path = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    assert not thought_path.exists()
    mock_upload_thought(conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20)
    user_dir = conf.DATA_DIR / str(conf.USER_20)
    assert user_dir.exists()
    assert user_dir.is_dir()
    assert thought_path.exists()
    assert thought_path.read_text() == conf.THOUGHT_20

    thought_path = _get_path(conf.DATA_DIR, conf.USER_22, conf.TIMESTAMP_22)
    assert not thought_path.exists()
    mock_upload_thought(conf, conf.USER_22, conf.TIMESTAMP_22, conf.THOUGHT_22)
    user_dir = conf.DATA_DIR / str(conf.USER_22)
    assert user_dir.exists()
    assert user_dir.is_dir()
    assert thought_path.exists()
    assert thought_path.read_text() == conf.THOUGHT_22


def test_race_condition(conf, server):
    timestamp = conf.TIMESTAMP_20
    for _ in range(10):
        timestamp += 1
        mock_upload_thought(conf, conf.USER_20, timestamp, conf.THOUGHT_20)
        mock_upload_thought(conf, conf.USER_20, timestamp, conf.THOUGHT_22)
        thought_path = _get_path(conf.DATA_DIR, conf.USER_20, timestamp)
        thoughts = set(thought_path.read_text().splitlines())
        assert thoughts == {conf.THOUGHT_20, conf.THOUGHT_22}


def test_partial_data(conf, server):
    message = \
        _serialize_thought(conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20)
    with socket.socket() as connection:
        time.sleep(0.1)  # Wait for server to start listening.
        connection.connect((conf.REQUEST_HOST, conf.SERVER_PORT))
        for c in message:
            connection.sendall(bytes([c]))
            time.sleep(0.01)
    thought_path = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    assert thought_path.read_text() == conf.THOUGHT_20
