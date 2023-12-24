import contextlib
import ctypes
import datetime as dt
import socket
import struct
import threading
import time

from brain_computer_interface import run_webserver
from brain_computer_interface.server import run_server
from brain_computer_interface.protocol import (
    TYPE_FORMAT,
    TYPE_FORMAT_SIZE,
    Types,
)
from brain_computer_interface.protocol import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    User,
)
from brain_computer_interface.utils.connection import Connection


_SERVER_BACKLOG = 1000
_HEADER_FORMAT = '<QQI'
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


class Dictionary(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)


def _run_server(conf):
    run_server(conf.LISTEN_HOST, conf.SERVER_PORT, conf.DATA_DIR)


def _run_webserver(conf):
    run_webserver(conf.LISTEN_HOST, conf.WEBSERVER_PORT, conf.DATA_DIR)


@contextlib.contextmanager
def _serve_thread(conf, serve):
    thread = threading.Thread(target=serve, args=(conf,))
    thread.start()
    time.sleep(1)
    yield thread
    _kill_serve_thread(thread)
    thread.join()


def _kill_serve_thread(thread: threading.Thread):
    if not thread.is_alive() or thread.ident is None:
        return
    c_thread_id = ctypes.c_long(thread.ident)
    c_key_board_interrupt = ctypes.py_object(KeyboardInterrupt)
    send_exception = ctypes.pythonapi.PyThreadState_SetAsyncExc
    res = send_exception(c_thread_id, c_key_board_interrupt)
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        send_exception(c_thread_id, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def _run_mock_server(conf, pipe):
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
        protocol_type = _receive_all(connection, TYPE_FORMAT_SIZE)
        protocol_type, = struct.unpack(TYPE_FORMAT, protocol_type)
        if protocol_type == Types.MIND.value:
            _receive_mind(connection, pipe)
        elif protocol_type == Types.THOUGHT.value:
            _receive_thought(connection, pipe)
        else:
            pass


def _receive_mind(connection, pipe):
    user = _receive_user(connection)
    _send_config(connection, Config(CONFIG_OPTIONS[:-1]))
    snapshot = _receive_snapshot(connection)
    pipe.send([user.serialize(), snapshot.serialize(), CONFIG_OPTIONS[-1]])


def _receive_user(connection) -> User:
    decoded_user_length = _receive_all(connection, Connection.length_size)
    user_length, = struct.unpack(
        Connection.length_format, decoded_user_length)
    return User.from_bytes(_receive_all(connection, user_length))


def _receive_snapshot(connection) -> Snapshot:
    decoded_snapshot_length = _receive_all(connection, Connection.length_size)
    snapshot_length, = struct.unpack(
        Connection.length_format, decoded_snapshot_length)
    return Snapshot.from_bytes(_receive_all(connection, snapshot_length))


def _send_config(connection, config: Config):
    config_data = config.serialize()
    config_len = struct.pack(Connection.length_format, len(config_data))
    connection.sendall(config_len)
    connection.sendall(config_data)


def _receive_thought(connection, pipe):
    header_data = _receive_all(connection, _HEADER_SIZE)
    user_id, timestamp, size = struct.unpack(_HEADER_FORMAT, header_data)
    data = _receive_all(connection, size)
    thought = data.decode()
    pipe.send([user_id, timestamp, thought])


def _receive_all(connection, size):
    chunks = []
    while size > 0:
        chunk = connection.recv(size)
        if not chunk:
            raise RuntimeError('incomplete data')
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)


def _assert_now(timestamp):
    now = int(time.time())
    assert abs(now - timestamp) < 5


def mock_upload_mind(conf, user: User, snapshot: Snapshot):
    with socket.socket() as connection:
        time.sleep(0.1)  # Wait for server to start listening.
        connection.settimeout(2)
        connection.connect((conf.REQUEST_HOST, conf.SERVER_PORT))
        connection.sendall(_serialize_user(user))
        config = _receive_config(connection)
        for c in CONFIG_OPTIONS:
            if c not in config:
                snapshot.set_default(c)
        connection.sendall(_serialize_snapshot(snapshot))
    time.sleep(0.2)  # Wait for server to write thought.


def mock_upload_thought(conf, user_id, timestamp, thought):
    message = _serialize_thought(user_id, timestamp, thought)
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
    decoded_config_length = _receive_all(connection, Connection.length_size)
    config_length, = struct.unpack(
        Connection.length_format, decoded_config_length)
    return Config.from_bytes(_receive_all(connection, config_length))


def _serialize_thought(user_id, timestamp, thought):
    protocol_type = struct.pack(TYPE_FORMAT, Types.THOUGHT.value)
    header = struct.pack(_HEADER_FORMAT, user_id, timestamp, len(thought))
    return protocol_type + header + thought.encode()


def _get_path(dir, user_id, timestamp):
    datetime = dt.datetime.fromtimestamp(timestamp)
    return dir / f'{user_id}/{datetime:%F_%H-%M-%S}.txt'
