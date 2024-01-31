import socket
import struct

from brain_computer_interface.message import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    User,
)
from brain_computer_interface.utils.connection import Connection

from tests.utils import receive_all


_SERVER_BACKLOG = 1000


def run_mock_server(conf, pipe):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((conf.LISTEN_HOST, conf.SERVER_PORT))
    server.listen(_SERVER_BACKLOG)
    pipe.send('ready')
    with server:
        while True:
            connection, address = server.accept()
            _handle_connection(connection, pipe)


def _handle_connection(connection, pipe):
    with connection:
        _receive_mind(connection, pipe)


def _receive_mind(connection, pipe):
    user = _receive_user(connection)
    _send_config(connection, Config(CONFIG_OPTIONS[:-1]))
    snapshots = list()
    while (decoded_snap := _receive_value_by_length(connection)) != b'done':
        snapshots.append(Snapshot.from_bytes(decoded_snap).serialize())
    pipe.send([user.serialize(), snapshots, CONFIG_OPTIONS[-1]])


def _receive_user(connection) -> User:
    return User.from_bytes(_receive_value_by_length(connection))


def _receive_value_by_length(connection) -> bytes:
    decoded_length = receive_all(connection, Connection.length_size)
    length, = struct.unpack(Connection.length_format, decoded_length)
    return receive_all(connection, length)


def _send_config(connection, config: Config):
    config_data = config.serialize()
    config_len = struct.pack(Connection.length_format, len(config_data))
    connection.sendall(config_len)
    connection.sendall(config_data)
