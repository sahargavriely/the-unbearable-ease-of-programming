import contextlib
import time
import pytest
import requests
import signal
import subprocess

from tests.rest.utils import Session


@pytest.fixture(scope='module')
def rest_server(conf):
    cmd = ['python', '-m', 'brain_computer_interface.rest', 'run-rest-server',
           '-h', conf.LISTEN_HOST, '-p', str(conf.REST_SERVER_PORT),
           '-d', conf.DATABASE_SCHEME]
    process = subprocess.Popen(cmd)
    try:
        yield process
    finally:
        # we are doing the sig thingy instead of terminate() or kill()
        # to increase coverage
        process.send_signal(signal.SIGINT)
        time.sleep(2)


@pytest.fixture(scope='module')
def client(rest_server, conf):
    yield rest_session(conf.REQUEST_HOST, conf.REST_SERVER_PORT)


def rest_session(host, port):
    session = Session(base_url=f'http://{host}:{port}')
    sec = 0
    timeout = 15
    interval = 0.5
    while sec < timeout:
        with contextlib.suppress(requests.ConnectionError):
            response = session.get('/')
            if response.status_code:
                break
        time.sleep(interval)
        sec += interval
    else:
        raise Exception('Session failed to connect rest server')
    return session
