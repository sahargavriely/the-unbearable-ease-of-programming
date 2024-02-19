import contextlib
import ctypes
import socket
import struct
import threading
import time

from brain_computer_interface.message import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    User,
)
from brain_computer_interface.utils.connection import Connection

from tests.utils import receive_all


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
    time.sleep(0.2)  # Wait for server to receive mind.


def _serialize_user(user):
    user_data = user.serialize()
    user_data_len = struct.pack(Connection.length_format, len(user_data))
    return user_data_len + user_data


def _serialize_snapshot(snapshot):
    snapshot_data = snapshot.serialize()
    snapshot_len = struct.pack(Connection.length_format, len(snapshot_data))
    return snapshot_len + snapshot_data


def _receive_config(connection) -> Config:
    decoded_config_length = receive_all(connection, Connection.length_size)
    config_length, = struct.unpack(
        Connection.length_format, decoded_config_length)
    return Config.from_bytes(receive_all(connection, config_length))


@contextlib.contextmanager
def serve_thread(serve, *args):
    thread = threading.Thread(target=serve, args=args)
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
