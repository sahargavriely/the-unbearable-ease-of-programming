import contextlib
from pathlib import Path
import socket
import struct
import threading

from ..utils import (
    Connection,
    DATA_DIR,
    Listener,
    LISTEN_HOST,
    SERVER_PORT,
    Thought,
)


def run_server(host: str = LISTEN_HOST, port: int = SERVER_PORT,
               data_dir: Path = DATA_DIR):
    lock = threading.Lock()
    with Listener(port, host) as listener:
        while True:
            try:
                with contextlib.suppress(socket.timeout):
                    connection = listener.accept()
                    thread = threading.Thread(
                        target = _handle_connection,
                        args = (lock, connection, data_dir),
                        daemon = True
                    )
                    thread.start()
            except KeyboardInterrupt:
                # exit gracefully
                break


def _handle_connection(lock: threading.Lock, connection: Connection,
                       data_dir: Path):
    with connection:
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
