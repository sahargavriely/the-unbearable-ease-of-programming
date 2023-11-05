import socket
import time

import pytest

from brain_computer_interface.utils import Connection


_DATA = b'Hello, world!'
_HOST = '127.0.0.1'
_PORT = 1234


@pytest.fixture
def server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', _PORT))
    server.listen(1000)
    try:
        time.sleep(0.1)
        yield server
    finally:
        server.close()


@pytest.fixture
def connection(server):
    sock = socket.socket()
    sock.connect((_HOST, _PORT))
    return Connection(sock)


def test_repr(connection: Connection):
    _, other_port = connection._socket.getsockname()
    assert connection.__repr__() == \
        f'<Connection from {_HOST}:{other_port} to {_HOST}:{_PORT}>'


def test_close(connection: Connection):
    assert not connection._socket._closed
    connection.close()
    assert connection._socket._closed


def test_send(server):
    connection = Connection.connect(_HOST, _PORT)
    with connection:
        client, _ = server.accept()
        connection.send(_DATA)
    chunks = []
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    assert b''.join(chunks) == _DATA


def test_receive(server):
    with Connection.connect(_HOST, _PORT) as connection:
        client, _ = server.accept()
        client.sendall(_DATA)
        assert connection.receive(len(_DATA)) == _DATA


def test_incomplete_data(server, connection: Connection):
    with connection:
        client, _ = server.accept()
        client.close()
        with pytest.raises(RuntimeError, match='Incomplete data'):
            connection.receive(1)
