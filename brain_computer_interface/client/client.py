import datetime as dt

from .reader import Reader
from ..message import (
    Config,
    CONFIG_OPTIONS,
)
from ..utils import (
    Connection,
    setup_logging,
    REQUEST_HOST,
    SERVER_PORT,
)

logger = setup_logging(__name__)


def upload_mind(path: str, host: str = REQUEST_HOST, port: int = SERVER_PORT):
    reader = Reader(path)
    logger.info('uploading user %s:', reader.user.name)
    with Connection.connect(host, port, 2) as connection:
        connection.send_length_follow_by_value(reader.user.serialize())
        decoded_conf = connection.receive_length_follow_by_value()
        config = Config.from_bytes(decoded_conf)
        for snapshot in reader:
            datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
            pretty_datetime = f'{datetime:%B %d, %Y at %T.%f}'
            logger.debug('uploading snapshot from %s:', pretty_datetime)
            for conf in CONFIG_OPTIONS:
                if conf not in config:
                    snapshot.set_default(conf)
            connection.send_length_follow_by_value(snapshot.serialize())
            print(f'{pretty_datetime} snapshot uploaded')
            logger.debug('done uploading snapshot from %s:', pretty_datetime)
        connection.send_length_follow_by_value(b'done')
    logger.info('done uploading user %s:', reader.user.name)
    print(f'{reader.user.name} uploaded')
