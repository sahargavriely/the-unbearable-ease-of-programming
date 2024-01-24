import json
from pathlib import Path
import pytest

from utils import _run_server, _serve_thread


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

    with _serve_thread(_run_server, write_data, conf) as thread:
        yield thread
