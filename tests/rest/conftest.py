import contextlib
import time
import pytest
import requests

from brain_computer_interface.rest import run_rest_server
from brain_computer_interface.rest.rest import collect_resource

from tests.rest.utils import Session
from tests.utils import serve_thread


@pytest.fixture(autouse=True, scope='session')
def addional_rest_requests():

    def error():
        raise Exception('Server error')

    collect_resource('/error')(error)


@pytest.fixture(scope='module')
def rest_server(conf):
    with serve_thread(_run_rest_server, conf) as thread:
        yield thread


def _run_rest_server(conf):

    run_rest_server(conf.LISTEN_HOST, conf.REST_SERVER_PORT,
                    conf.DATABASE_SCHEME)


@pytest.fixture(scope='module')
def client(conf):
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
