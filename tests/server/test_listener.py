import multiprocessing
import socket
import time

import pytest

from brain_computer_interface.server.listener import Listener
from brain_computer_interface.utils import Connection


_PORT = 5914
_HOST = '127.0.0.1'
_BACKLOG = 5000
_REUSEADDR = True
_TIMEOUT = 2
_DATA = b'Hello, world!'


@pytest.fixture
def listener():
    return Listener(_PORT, _HOST, _BACKLOG, _REUSEADDR, _TIMEOUT)


def test_defaults_and_edges():
    listener = Listener(_PORT, reuseaddr=False)
    assert listener.host == '0.0.0.0'
    assert listener.backlog == 1000
    assert not listener.reuseaddr
    assert listener.timeout


def test_attributes(listener: Listener):
    assert listener.port == _PORT
    assert listener.host == _HOST
    assert listener.backlog == _BACKLOG
    assert listener.reuseaddr == _REUSEADDR
    assert listener.timeout == _TIMEOUT


def test_repr(listener: Listener):
    assert listener.__repr__() == f'Listener(port={_PORT!r}, ' \
        f'host={_HOST!r}, backlog={_BACKLOG!r}, ' \
        f'reuseaddr={_REUSEADDR!r}, timeout={_TIMEOUT!r})'


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


def test_load(listener: Listener):
    with listener:
        time.sleep(0.1)
        amount = 9900
        args = [Connection.connect(_HOST, _PORT), amount]
        p = multiprocessing.Process(target=_send_loads, args=args, daemon=True)
        p.start()
        count = 0
        with listener.accept() as client:
            with pytest.raises(socket.timeout):
                while client.receive_length_follow_by_value() == _DATA:
                    count += 1
            assert count == amount
        p.terminate()
        p.join(2)


def _send_loads(conn: Connection, amount):
    with conn:
        for _ in range(amount):
            conn.send_length_follow_by_value(_DATA)
