import datetime as dt

from ..utils import (
    Connection,
    REQUEST_HOST,
    SERVER_PORT,
    Thought,
)


def upload_thought(user_id: int, thought: str, host: str = REQUEST_HOST,
                   port: int = SERVER_PORT):
    thought_obj = Thought(user_id, dt.datetime.now(), thought)
    with Connection.connect(host, port) as connection:
        connection.send(thought_obj.serialize())
    print('done')
