
import datetime as dt
from pathlib import Path
import multiprocessing
import shutil

import pytest

from brain_computer_interface.utils import config

from utils import (
    Dictionary,
    _run_server,
    _run_webserver,
    _run_mock_server,
    _serve_thread,
)


@pytest.fixture(scope='session')
def other_conf():
    return Dictionary({
        'USER_20': 20,
        'THOUGHT_20': 'I am 20 too',
        'TIMESTAMP_20':
            int(dt.datetime(2019, 10, 25, 15, 12, 5, 228000).timestamp()),
        'USER_22': 22,
        'THOUGHT_22': 'I am 22',
        'TIMESTAMP_22':
            int(dt.datetime(2019, 10, 25, 15, 15, 2, 304000).timestamp()),
    })


@pytest.fixture(scope='session')
def patch_conf(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp('data')
    return Dictionary({
        'DATA_DIR': Path(tmp_path),
        'LISTEN_HOST': '0.0.0.0',
        'REQUEST_HOST': '127.0.0.1',
        'SERVER_PORT': 5356,
        'WEBSERVER_PORT': 8356,
    })


@pytest.fixture(scope='session')
def conf(patch_conf, other_conf):
    other_conf.update(patch_conf)
    other_conf.WEBSERVER_URL = \
        f'http://{other_conf.REQUEST_HOST}:{other_conf.WEBSERVER_PORT}'
    return other_conf


@pytest.fixture(autouse=True)
def patch(monkeypatch, patch_conf):
    for key, value in patch_conf.items():
        monkeypatch.setattr(config, key, value)


@pytest.fixture(autouse=True)
def clean_db(conf):
    if conf.DATA_DIR.exists():
        shutil.rmtree(str(conf.DATA_DIR))


@pytest.fixture(scope='module')
def server(conf):
    with _serve_thread(conf, _run_server) as thread:
        yield thread


@pytest.fixture(scope='module')
def webserver(conf):
    with _serve_thread(conf, _run_webserver) as thread:
        yield thread


@pytest.fixture
def mock_server(conf):
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_mock_server,
                                      args=(conf, child))
    process.start()
    parent.recv()
    yield parent
    process.terminate()
    process.join()


@pytest.fixture
def get_message(mock_server):

    def get_message():
        if not mock_server.poll(1):
            raise TimeoutError()
        return mock_server.recv()

    yield get_message
