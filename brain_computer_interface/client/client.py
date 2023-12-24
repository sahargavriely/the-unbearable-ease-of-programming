import datetime as dt
from struct import pack

from .reader import Reader
from ..protocol import (
    Config,
    CONFIG_OPTIONS,
    Types,
    TYPE_FORMAT,
)
from ..utils import (
    Connection,
    setup_logging,
    REQUEST_HOST,
    SERVER_PORT,
    Thought,
)

logger = setup_logging(__name__)


def upload_mind(path: str, host: str = REQUEST_HOST, port: int = SERVER_PORT):
    reader = Reader(path)
    logger.info('uploading user %s:', reader.user.name)
    for snapshot in reader:
        # we are opening new connection on every snapshot
        # to simulate a real scenario
        datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
        pretty_print_datetime = f'{datetime:%B %d, %Y at %T.%f}'
        with Connection.connect(host, port) as connection:
            logger.debug('uploading snapshot from %s:', pretty_print_datetime)
            _send_type(connection, Types.MIND)
            connection.send_length_follow_by_value(reader.user.serialize())
            decoded_conf = connection.receive_length_follow_by_value()
            config = Config.from_bytes(decoded_conf)
            for conf in CONFIG_OPTIONS:
                if conf not in config:
                    delattr(snapshot, conf)
            connection.send_length_follow_by_value(snapshot.serialize())
        print(f'{pretty_print_datetime} snapshot uploaded')
        logger.debug('done uploading snapshot from %s:', pretty_print_datetime)
    logger.info('done uploading user %s:', reader.user.name)
    print(f'{reader.user.name} uploaded')


def upload_thought(user_id: int, thought: str, host: str = REQUEST_HOST,
                   port: int = SERVER_PORT):
    logger.info('uploading thought of user %s:', user_id)
    thought_obj = Thought(user_id, dt.datetime.now(), thought)
    with Connection.connect(host, port) as connection:
        _send_type(connection, Types.THOUGHT)
        connection.send(thought_obj.serialize())
    logger.info('done uploading thought of user %s:', user_id)
    print('done')


def _send_type(connection: Connection, protocol_type: Types):
    connection.send(pack(TYPE_FORMAT, protocol_type.value))
