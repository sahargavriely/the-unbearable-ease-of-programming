import concurrent.futures as cf
import contextlib
import datetime as dt
from pathlib import Path
import socket
import threading
import typing

from .listener import Listener
from ..distributer import Distributer
from ..message import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    User,
)
from ..utils import (
    Connection,
    keys,
    LISTEN_HOST,
    DISTRIBUTE_SCHEME,
    SERVER_PORT,
    setup_logging,
    SHARED_DIR,
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

    with cf.ThreadPoolExecutor(5) as executor:
        with Listener(port, host) as listener:
            while True:
                try:
                    with contextlib.suppress(socket.timeout):
                        connection = listener.accept()
                        executor.submit(_handle_connection, lock,
                                        connection, publish_method, shared_dir)
                except KeyboardInterrupt:
                    # exit gracefully
                    break


def _handle_connection(lock: threading.Lock, connection: Connection,
                       publish_method: typing.Callable, shared_dir: Path):
    with connection:
        _recive_mind(lock, connection, publish_method, shared_dir)


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
