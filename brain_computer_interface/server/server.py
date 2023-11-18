import contextlib
from pathlib import Path
import socket
import struct
import threading

from .parser import Parser
from .parsers import parsers
from ..utils import (
    Connection,
    Config,
    DATA_DIR,
    Listener,
    LISTEN_HOST,
    SERVER_PORT,
    Snapshot,
    Thought,
    TYPE_FORMAT,
    TYPE_SIZE,
    Types,
    User,
)


def run_server(host: str = LISTEN_HOST, port: int = SERVER_PORT, data_dir: Path = DATA_DIR):
    lock = threading.Lock()
    
    parser = Parser(data_dir=data_dir)
    for parser_name, obj in parsers:
        parser(parser_name)(obj)

    with Listener(port, host) as listener:
        while True:
            try:
                with contextlib.suppress(socket.timeout):
                    connection = listener.accept()
                    thread = threading.Thread(
                        target = _handle_connection,
                        args = (lock, connection, data_dir, parser),
                        daemon = True
                    )
                    thread.start()
            except KeyboardInterrupt:
                # exit gracefully
                break


def _handle_connection(lock: threading.Lock, connection: Connection, data_dir: Path, parser: Parser):
    with connection:
        protocol_type = _receive_type(connection)
        if protocol_type == Types.MIND.value:
            _recive_mind(connection, lock, data_dir, parser)
        elif protocol_type == Types.THOUGHT.value:
            _recive_thought(connection, lock, data_dir)
        else:
            pass


def _recive_mind(connection: Connection, lock, data_dir: Path, parser: Parser):
    user = User.from_bytes(connection.receive_length_follow_by_value())
    config_request = Config(['timestamp', *parser.parsers.keys()])
    connection.send_length_follow_by_value(config_request.serialize())
    snapshot = Snapshot.from_bytes(connection.receive_length_follow_by_value())
    cur_user_dir = data_dir / str(user.id) / f'{snapshot.timestamp:%F_%H-%M-%S-%f}'
    with lock:
        cur_user_dir.mkdir(parents=True, exist_ok=True)
        parser.parse(cur_user_dir, snapshot)


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
    protocol_type = connection.receive(TYPE_SIZE)
    protocol_type, = struct.unpack(TYPE_FORMAT, protocol_type)
    return protocol_type
