import datetime as dt
from http import HTTPStatus
import signal
import subprocess
import time

import requests

from brain_computer_interface.protocol import (
    Snapshot,
    User,
)
from utils import (
    _assert_now,
    _get_path,
    mock_upload_mind,
    mock_upload_thought,
)


def test_read(mind_file, snapshot: Snapshot, user: User):
    cmd = ['python', '-m', 'brain_computer_interface', 'read', str(mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert repr(user) in stdout.decode()
    assert repr(snapshot) in stdout.decode()


def test_compressed_read(compressed_mind_file, snapshot: Snapshot, user: User):
    cmd = ['python', '-m', 'brain_computer_interface', 'read',
           str(compressed_mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert repr(user) in stdout.decode()
    assert repr(snapshot) in stdout.decode()


def test_upload_mind(conf, mind_file, compressed_mind_file, user, snapshot,
                     get_message):
    cmd = ['python', '-m', 'brain_computer_interface', 'client', 'upload-mind',
           '-h', conf.REQUEST_HOST, '-p', str(conf.SERVER_PORT),
           str(mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'complete snapshot' in stdout.lower()
    assert b'complete user' in stdout.lower()
    decoded_user, decoded_snapshot, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert decoded_snapshot == snapshot.serialize()

    cmd = ['python', '-m', 'brain_computer_interface', 'client', 'upload-mind',
           '-h', conf.REQUEST_HOST, '-p', str(conf.SERVER_PORT),
           str(compressed_mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'complete snapshot' in stdout.lower()
    assert b'complete user' in stdout.lower()
    decoded_user, decoded_snapshot, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert decoded_snapshot == snapshot.serialize()


def test_upload_thought(conf, get_message):
    cmd = ['python', '-m', 'brain_computer_interface', 'client',
           'upload-thought', '-h', conf.REQUEST_HOST,
           '-p', str(conf.SERVER_PORT), str(conf.USER_20), conf.THOUGHT_20]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'done' in stdout.lower()
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_20
    _assert_now(timestamp)
    assert thought == conf.THOUGHT_20


def test_upload_thought_error(conf):
    cmd = ['python', '-m', 'brain_computer_interface', 'client',
           'upload-thought', '-h', conf.REQUEST_HOST,
           '-p', str(conf.SERVER_PORT), str(conf.USER_20), conf.THOUGHT_20]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert b'error' in stdout.lower()


def test_run_server(conf, user, snapshot):
    cmd = ['python', '-m', 'brain_computer_interface', 'run-server',
           '-h', conf.LISTEN_HOST, '-p', str(conf.SERVER_PORT),
           '-d', str(conf.DATA_DIR)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    try:
        time.sleep(0.4)
        args = conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20
        mock_upload_thought(*args)
        args = conf, conf.USER_22, conf.TIMESTAMP_22, conf.THOUGHT_22
        mock_upload_thought(*args)
        mock_upload_mind(conf, user, snapshot)
        time.sleep(0.1)
    finally:
        # we are doing the sig thingy instead of terminate to increase coverage
        process.send_signal(signal.SIGINT)
    thought_path_1 = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    thought_path_2 = _get_path(conf.DATA_DIR, conf.USER_22, conf.TIMESTAMP_22)
    assert thought_path_1.read_text() == conf.THOUGHT_20
    assert thought_path_2.read_text() == conf.THOUGHT_22
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    mind_path = conf.DATA_DIR / f'{user.id}/{datetime:%F_%H-%M-%S-%f}'
    assert mind_path.exists()
    assert mind_path.is_dir()


def test_run_webserver(conf):
    cmd = ['python', '-m', 'brain_computer_interface', 'run-webserver',
           '-h', conf.LISTEN_HOST, '-p', str(conf.WEBSERVER_PORT),
           '-d', str(conf.DATA_DIR)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    try:
        time.sleep(1)
        response = requests.get(conf.WEBSERVER_URL)
        assert response.status_code == HTTPStatus.OK
        assert 'Brain Computer Interface' in response.text
    finally:
        # we are doing the sig thingy instead of terminate to increase coverage
        process.send_signal(signal.SIGINT)


def test_error():
    cmd = ['python', '-m', 'brain_computer_interface', 'error']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout, _ = process.communicate()
    assert b'something went terribly wrong :[' in stdout.lower()


def test_quiet_flag():
    cmd = ['python', '-m', 'brain_computer_interface', '-q', 'error']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout, _ = process.communicate()
    assert not stdout.lower()


def test_traceback_flag():
    cmd = ['python', '-m', 'brain_computer_interface', '-t', 'error']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout, _ = process.communicate()
    assert b'traceback (most recent call last)' in stdout.lower()
