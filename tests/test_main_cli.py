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
