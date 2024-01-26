import datetime as dt

import furl

from ..utils import (
    DATABASE_SCHEME,
    get_driver,
    setup_logging
)


logger = setup_logging(__name__)


class Database:

    def __init__(self, url: str = DATABASE_SCHEME):
        logger.info('initiating database for url %s', url)
        url_ = furl.furl(url)
        self.driver = get_driver(
            __file__, __package__, 'scheme', url_.scheme)(url_)

    def save_user(self, user_id: int, data: dict):
        logger.info('saving to user id %s', user_id)
        self.driver.save_user(user_id, data)

    def save_snapshot_topic(self, user_id: int, datetime: int, topic: str,
                            data: dict):
        logger.info('saving %s of user id %s snapshot at datetime %s',
                    topic, user_id, datetime)
        self.driver.save_snapshot_topic(user_id, datetime, topic, data)

    def get_users(self) -> list:
        logger.info('getting all users')
        return self.driver.get_users()

    def get_user(self, user_id: int) -> dict:
        logger.info('getting user id %s', user_id)
        user = self.driver.get_user(user_id)
        if not user:
            raise ValueError(f'User id {user_id!r} does not exists')
        return user

    def get_user_snapshots(self, user_id: int) -> list:
        logger.info('getting user id %s snapshots', user_id)
        return self.driver.get_user_snapshots(user_id)

    def get_user_snapshot(self, user_id: int, datetime: int) -> dict:
        logger.info('getting user id %s snapshot at datetime %s',
                    user_id, datetime)
        snapshot = self.driver.get_user_snapshot(user_id, datetime)
        if not snapshot:
            datetime_ = dt.datetime.fromtimestamp(datetime / 1000)
            raise ValueError(f'User id {user_id!r} does not have '
                             f'snapshot from {datetime_:%F_%H-%M-%S-%f}')
        return snapshot

    def get_user_snapshot_topic(self, user_id: int, datetime: int,
                                topic: str) -> dict:
        logger.info('getting %s of user id %s snapshot at datetime %s',
                    topic, user_id, datetime)
        data = self.driver.get_user_snapshot_topic(user_id, datetime, topic)
        if not data:
            datetime_ = dt.datetime.fromtimestamp(datetime / 1000)
            raise ValueError(f'User id {user_id!r} snapshot from '
                             f'{datetime_:%F_%H-%M-%S-%f} does not '
                             f'have {topic!r}')
        return data

    def drop_db(self):
        self.driver.drop_db()
