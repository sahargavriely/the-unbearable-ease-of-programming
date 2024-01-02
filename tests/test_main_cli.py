from http import HTTPStatus
import signal
import subprocess
import time

import requests


def test_run_webserver(conf):
    cmd = ['python', '-m', 'brain_computer_interface', 'run-webserver',
           '-h', conf.LISTEN_HOST, '-p', str(conf.WEBSERVER_PORT),
           '-d', str(conf.SHARED_DIR)]
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
