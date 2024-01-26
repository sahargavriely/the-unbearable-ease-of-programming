import datetime as dt
import socket
import struct
import time

from brain_computer_interface.message import (
    TYPE_FORMAT,
    Types,
)
from brain_computer_interface.message import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    User,
)
from brain_computer_interface.utils.connection import Connection

from tests.utils import receive_all


_HEADER_FORMAT = '<QQI'


def get_path(dir, user_id, timestamp):
    datetime = dt.datetime.fromtimestamp(timestamp)
    return dir / f'{user_id}/{datetime:%F_%H-%M-%S}.txt'


def mock_upload_mind(conf, user: User, *snapshots: Snapshot):
    with socket.socket() as connection:
        time.sleep(0.1)  # Wait for server to start listening.
        connection.connect((conf.REQUEST_HOST, conf.SERVER_PORT))
        connection.sendall(_serialize_user(user))
        config = _receive_config(connection)
        for snapshot in snapshots:
            for c in CONFIG_OPTIONS:
                if c not in config:
                    snapshot.set_default(c)
            connection.sendall(_serialize_snapshot(snapshot))
        data = b'done'
        length = struct.pack(Connection.length_format, len(data))
        connection.sendall(length)
        connection.sendall(data)
    time.sleep(0.2)  # Wait for server to write thought.


def mock_upload_thought(conf, user_id, timestamp, thought):
    message = serialize_thought(user_id, timestamp, thought)
    with socket.socket() as connection:
        time.sleep(0.1)  # Wait for server to start listening.
        connection.settimeout(2)
        connection.connect((conf.REQUEST_HOST, conf.SERVER_PORT))
        connection.sendall(message)
    time.sleep(0.2)  # Wait for server to write thought.


def _serialize_user(user):
    protocol_type = struct.pack(TYPE_FORMAT, Types.MIND.value)
    user_data = user.serialize()
    user_data_len = struct.pack(Connection.length_format, len(user_data))
    return protocol_type + user_data_len + user_data


def _serialize_snapshot(snapshot):
    snapshot_data = snapshot.serialize()
    snapshot_len = struct.pack(Connection.length_format, len(snapshot_data))
    return snapshot_len + snapshot_data


def _receive_config(connection) -> Config:
    decoded_config_length = receive_all(connection, Connection.length_size)
    config_length, = struct.unpack(
        Connection.length_format, decoded_config_length)
    return Config.from_bytes(receive_all(connection, config_length))


def serialize_thought(user_id, timestamp, thought):
    protocol_type = struct.pack(TYPE_FORMAT, Types.THOUGHT.value)
    header = struct.pack(_HEADER_FORMAT, user_id, timestamp, len(thought))
    return protocol_type + header + thought.encode()
