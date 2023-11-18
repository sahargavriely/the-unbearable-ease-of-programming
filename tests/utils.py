import contextlib
import ctypes
import datetime as dt
import socket
import struct
import threading
import time

from brain_computer_interface import run_server, run_webserver
from brain_computer_interface.utils import (
    TYPE_FORMAT,
    TYPE_SIZE,
    Types,
)


_SERVER_BACKLOG = 1000
_HEADER_FORMAT = 'LLI'
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
        protocol_type = _receive_all(connection, TYPE_SIZE)  # ignore for now
        protocol_type, = struct.unpack(TYPE_FORMAT, protocol_type)  # ignore for now
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


def mock_upload_thought(conf, user_id, timestamp, thought):
    message = _serialize_thought(user_id, timestamp, thought)
    with socket.socket() as connection:
        time.sleep(0.1)  # Wait for server to start listening.
        connection.settimeout(2)
        connection.connect((conf.REQUEST_HOST, conf.SERVER_PORT))
        connection.sendall(message)
    time.sleep(0.2)  # Wait for server to write thought.


def _serialize_thought(user_id, timestamp, thought):
    protocol_type = struct.pack(TYPE_FORMAT, Types.THOUGHT.value)
    header = struct.pack(_HEADER_FORMAT, user_id, timestamp, len(thought))
    return protocol_type + header + thought.encode()


def _get_path(dir, user_id, timestamp):
    datetime = dt.datetime.fromtimestamp(timestamp)
    return dir / f'{user_id}/{datetime:%F_%H-%M-%S}.txt'
