from http import HTTPStatus
import signal
import subprocess
import time

import requests

from utils import (
    _assert_now,
    _get_path,
    mock_upload_thought,
)


def test_upload_thought(conf, get_message):
    cmd = ['python', '-m', 'brain_computer_interface', 'upload-thought',
           '-h', conf.REQUEST_HOST, '-p', str(conf.SERVER_PORT),
           str(conf.USER_20), conf.THOUGHT_20]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'done' in stdout.lower()
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_20
    _assert_now(timestamp)
    assert thought == conf.THOUGHT_20


def test_upload_thought_error(conf):
    cmd = ['python', '-m', 'brain_computer_interface', 'upload-thought',
           '-h', conf.REQUEST_HOST, '-p', str(conf.SERVER_PORT),
           str(conf.USER_20), conf.THOUGHT_20]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert b'error' in stdout.lower()


def test_run_server(conf):
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
        time.sleep(0.1)
    finally:
        # we are doing the sig thingy instead of terminate to increase coverage
        process.send_signal(signal.SIGINT)
    thought_path_1 = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    thought_path_2 = _get_path(conf.DATA_DIR, conf.USER_22, conf.TIMESTAMP_22)
    assert thought_path_1.read_text() == conf.THOUGHT_20
    assert thought_path_2.read_text() == conf.THOUGHT_22


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
