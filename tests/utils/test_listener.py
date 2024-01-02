import socket
import time

import pytest

from brain_computer_interface.utils import Listener


_PORT = 5914
_HOST = '127.0.0.1'
_BACKLOG = 5000
_REUSEADDR = True
_DATA = b'Hello, world!'


@pytest.fixture
def listener():
    return Listener(_PORT, _HOST, _BACKLOG, _REUSEADDR)


def test_defaults():
    listener = Listener(_PORT)
    assert listener.host == '0.0.0.0'
    assert listener.backlog == 1000
    assert listener.reuseaddr


def test_attributes(listener: Listener):
    assert listener.port == _PORT
    assert listener.host == _HOST
    assert listener.backlog == _BACKLOG
    assert listener.reuseaddr == _REUSEADDR


def test_repr(listener: Listener):
    assert listener.__repr__() == f'Listener(port={_PORT!r}, ' \
        f'host={_HOST!r}, backlog={_BACKLOG!r}, reuseaddr={_REUSEADDR!r})'


def test_close(listener: Listener):
    assert socket.socket().connect_ex((_HOST, _PORT))
    listener.start()
    try:
        time.sleep(0.1)
        assert not socket.socket().connect_ex((_HOST, _PORT))
    finally:
        listener.stop()
    assert socket.socket().connect_ex((_HOST, _PORT))


def test_accept(listener: Listener):
    sock = socket.socket()
    with listener:
        time.sleep(0.1)
        sock.connect((_HOST, _PORT))
        connection = listener.accept()
        try:
            sock.sendall(_DATA)
            assert connection.receive(len(_DATA)) == _DATA
        finally:
            connection.close()
