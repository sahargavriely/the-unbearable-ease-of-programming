import socket
import time

from utils import (
    _get_path,
    mock_upload_thought,
    _serialize_thought,
)


def test_user_id(conf, server):
    mock_upload_thought(conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20)
    user_dir = conf.DATA_DIR / str(conf.USER_20)
    assert user_dir.exists()
    assert user_dir.is_dir()
    mock_upload_thought(conf, conf.USER_22, conf.TIMESTAMP_20, conf.THOUGHT_20)
    user_dir = conf.DATA_DIR / str(conf.USER_22)
    assert user_dir.exists()
    assert user_dir.is_dir()


def test_timestamp(conf, server):
    thought_path = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    assert not thought_path.exists()
    mock_upload_thought(conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20)
    assert thought_path.exists()
    thought_path = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_22)
    assert not thought_path.exists()
    mock_upload_thought(conf, conf.USER_20, conf.TIMESTAMP_22, conf.THOUGHT_20)
    assert thought_path.exists()


def test_thought(conf, server):
    mock_upload_thought(conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20)
    thought_path = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    assert thought_path.read_text() == conf.THOUGHT_20
    mock_upload_thought(conf, conf.USER_22, conf.TIMESTAMP_22, conf.THOUGHT_22)
    thought_path = _get_path(conf.DATA_DIR, conf.USER_22, conf.TIMESTAMP_22)
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
