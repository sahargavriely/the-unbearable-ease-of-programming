import contextlib
import datetime as dt
from pathlib import Path
import socket
import struct
import threading
import typing

from ..distributer import Distributer
from ..message import (
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
    keys,
    Listener,
    LISTEN_HOST,
    DISTRIBUTE_SCHEME,
    SERVER_PORT,
    setup_logging,
    SHARED_DIR,
    Thought,
)


logger = setup_logging(__name__)


def run_server_by_scheme(distribute_scheme: str = DISTRIBUTE_SCHEME,
                         host: str = LISTEN_HOST, port: int = SERVER_PORT,
                         shared_dir: Path = SHARED_DIR):
    with Distributer(distribute_scheme) as distributer:
        run_server(distributer.publish_server, host, port, shared_dir)


def run_server(publish_method: typing.Callable,
               host: str = LISTEN_HOST, port: int = SERVER_PORT,
               shared_dir: Path = SHARED_DIR):
    logger.info('starting server on %s:%s and shared directory at %s',
                host, port, shared_dir)
    lock = threading.Lock()

    with Listener(port, host) as listener:
        while True:
            try:
                with contextlib.suppress(socket.timeout):
                    connection = listener.accept()
                    thread = threading.Thread(
                        target = _handle_connection,
                        args = (lock, connection, publish_method, shared_dir),
                        daemon = True
                    )
                    thread.start()
            except KeyboardInterrupt:
                # exit gracefully
                break


def _handle_connection(lock: threading.Lock, connection: Connection,
                       publish_method: typing.Callable, shared_dir: Path):
    with connection:
        protocol_type = _receive_type(connection)
        if protocol_type == Types.MIND.value:
            _recive_mind(lock, connection, publish_method, shared_dir)
        elif protocol_type == Types.THOUGHT.value:
            _recive_thought(connection, lock, shared_dir)


def _recive_mind(lock: threading.Lock, connection: Connection,
                 publish_method: typing.Callable, shared_dir: Path):
    user = User.from_bytes(connection.receive_length_follow_by_value())
    user_id = str(user.id)
    logger.debug('receiving mind from user %s', user_id)
    user = user.jsonify()
    publish_method({keys.user: user})
    config_request = Config(CONFIG_OPTIONS)  # TODO = available parsers
    connection.send_length_follow_by_value(config_request.serialize())
    while (byte_snapshot := connection.receive_length_follow_by_value()) \
            != b'done':
        snapshot = Snapshot.from_bytes(byte_snapshot)
        datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
        imgs_dir = shared_dir / user_id / f'{datetime:%F_%H-%M-%S-%f}'
        logger.debug('creating images shared directory at %s', imgs_dir)
        imgs_dir.mkdir(parents=True, exist_ok=True)
        with lock:
            json_snapshot = snapshot.jsonify(imgs_dir)
        publish_method({
            keys.user: user,
            keys.snapshot: json_snapshot
        })


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
