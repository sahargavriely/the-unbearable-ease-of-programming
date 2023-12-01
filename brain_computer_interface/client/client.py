import datetime as dt
from struct import pack

from ..protocol import (
    Config,
    Types,
    TYPE_FORMAT,
)
from ..reader import Reader
from ..utils import (
    Connection,
    REQUEST_HOST,
    SERVER_PORT,
    Thought,
)


def upload_mind(path: str, host: str = REQUEST_HOST, port: int = SERVER_PORT):
    reader = Reader(path)
    for snapshot in reader:
        # we are opening new connection on every snapshot to simulate a real scenario
        with Connection.connect(host, port) as connection:
            _send_type(connection, Types.MIND)
            connection.send_length_follow_by_value(reader.user.serialize())
            config = Config.from_bytes(connection.receive_length_follow_by_value())
            for conf in snapshot.config:
                if conf not in config:
                    snapshot.set_default(conf)
            connection.send_length_follow_by_value(snapshot.serialize())
        print('complete snapshot')
    print('complete user')


def upload_thought(user_id: int, thought: str, host: str = REQUEST_HOST,
                   port: int = SERVER_PORT):
    thought_obj = Thought(user_id, dt.datetime.now(), thought)
    with Connection.connect(host, port) as connection:
        _send_type(connection, Types.THOUGHT)
        connection.send(thought_obj.serialize())
    print('done')


def _send_type(connection: Connection, protocol_type: Types):
    connection.send(pack(TYPE_FORMAT, protocol_type.value))
