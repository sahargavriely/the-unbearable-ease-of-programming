import pytest

from brain_computer_interface.rest import run_rest_server

from tests.utils import serve_thread


@pytest.fixture(scope='module')
def rest_server(conf):
    with serve_thread(_run_rest_server, conf) as thread:
        yield thread


def _run_rest_server(conf):
    run_rest_server(conf.LISTEN_HOST, conf.REST_SERVER_PORT,
                    conf.DATABASE_SCHEME)
