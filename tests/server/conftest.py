import json
from pathlib import Path
import pytest

from brain_computer_interface.server import run_server

from tests.utils import serve_thread


@pytest.fixture(scope='module')
def server_publish_file(tmp_path_factory):
    return tmp_path_factory.mktemp('publish') / 'data.json'


@pytest.fixture(autouse=True)
def clean_server_publish_file(server_publish_file):
    if server_publish_file.exists():
        server_publish_file.unlink()


@pytest.fixture(scope='module')
def server(conf, server_publish_file: Path):

    def write_data(data):
        with server_publish_file.open('w') as file:
            json.dump(data, file)

    with serve_thread(_run_server, write_data, conf) as thread:
        yield thread


def _run_server(publish_method, conf):
    run_server(publish_method, conf.LISTEN_HOST,
               conf.SERVER_PORT, conf.SHARED_DIR)
