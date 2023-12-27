import contextlib
import datetime as dt
import functools
from pathlib import Path
import socket
import struct
import threading
import typing

from furl import furl

from .publish_schemes import schemes
from ..protocol import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    Types,
    TYPE_FORMAT,
    TYPE_FORMAT_SIZE,
    User,
)
from ..utils import (
    Connection,
    DATA_DIR,
    Listener,
    LISTEN_HOST,
    PUBLISH_SCHEME,
    SERVER_PORT,
    Thought,
)


def run_server_by_scheme(publish_scheme: str = PUBLISH_SCHEME,
                         host: str = LISTEN_HOST, port: int = SERVER_PORT):
    url = furl(publish_scheme)
    publish_method = schemes.get(url.scheme)
    if not publish_method:
        raise ValueError(f'Publish scheme {url.scheme!r} not supported :[')
    publish_method = functools.partial(publish_method, url)
    run_server(publish_method, host, port)


def run_server(publish_method: typing.Callable,
               host: str = LISTEN_HOST, port: int = SERVER_PORT,
               data_dir: Path = DATA_DIR):
    lock = threading.Lock()

    with Listener(port, host) as listener:
        while True:
            try:
                with contextlib.suppress(socket.timeout):
                    connection = listener.accept()
                    thread = threading.Thread(
                        target = _handle_connection,
                        args = (lock, connection, publish_method, data_dir),
                        daemon = True
                    )
                    thread.start()
            except KeyboardInterrupt:
                # exit gracefully
                break


def _handle_connection(lock: threading.Lock, connection: Connection,
                       publish_method, data_dir: Path):
    with connection:
        protocol_type = _receive_type(connection)
        if protocol_type == Types.MIND.value:
            _recive_mind(connection, publish_method, lock, data_dir)
        elif protocol_type == Types.THOUGHT.value:
            _recive_thought(connection, lock, data_dir)
        else:
            pass


def _recive_mind(connection: Connection, publish_method: typing.Callable,
                 lock: threading.Lock, shared_dir: Path):
    user = User.from_bytes(connection.receive_length_follow_by_value())
    config_request = Config(CONFIG_OPTIONS)  # TODO = available parsers
    connection.send_length_follow_by_value(config_request.serialize())
    snapshot = Snapshot.from_bytes(connection.receive_length_follow_by_value())
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    imgs_dir = shared_dir / str(user.id) / f'{datetime:%F_%H-%M-%S-%f}'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    with lock:
        json_snapshot = snapshot.jsonify(imgs_dir)
    publish_method(user.jsonify(), json_snapshot)


def _recive_thought(connection: Connection, lock, data_dir: Path):
    headers = connection.receive(Thought.header_size)
    _, _, size = struct.unpack(Thought.header_format, headers)
    data = connection.receive(size)
    thought = Thought.deserialize(headers + data)
    with lock:
        _handle_thought(data_dir, thought)


def _handle_thought(data_dir: Path, thought: Thought):
    timestamp = thought.file_formatted_timestamp
    user_dir = data_dir / str(thought.user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    file_path = user_dir / f'{timestamp}.txt'
    to_write = thought.thought
    if file_path.exists():
        to_write = f'\n{thought.thought}'
    with file_path.open('a') as file:
        file.write(to_write)


def _receive_type(connection: Connection):
    protocol_type = connection.receive(TYPE_FORMAT_SIZE)
    protocol_type, = struct.unpack(TYPE_FORMAT, protocol_type)
    return protocol_type
