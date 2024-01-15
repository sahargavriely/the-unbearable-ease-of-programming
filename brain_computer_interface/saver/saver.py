import furl

from ..distributer import Distributer
from ..utils import get_driver, keys, setup_logging


logger = setup_logging(__name__)


class Saver:
    group = 'saver'

    def __init__(self, url: str):
        logger.info('initiating saver for url %s', url)
        url_ = furl.furl(url)
        self.driver = get_driver(
            __file__, __package__, 'scheme', url_.scheme)(url_)

    def save_user(self, user_id, data):
        logger.info('saving to user id %s', user_id)
        self.driver.save_user(user_id, data)

    def save_snapshot_topic(self, topic, user_id, datetime, data):
        logger.info('saving %s of user id %s snapshot at datetime %s',
                    topic, user_id, datetime)
        self.driver.save_snapshot_topic(topic, user_id, datetime, data)

    def get_user(self, user_id):
        logger.info('getting user id %s', user_id)
        return self.driver.get_user(user_id)

    def get_user_snapshots(self, user_id):
        logger.info('getting user id %s snapshots', user_id)
        return self.driver.get_user_snapshots(user_id)

    def get_snapshot_topic(self, topic, user_id, datetime):
        logger.info('getting %s of user id %s snapshot at datetime %s',
                    topic, user_id, datetime)
        return self.driver.get_snapshot_topic(topic, user_id, datetime)

    @classmethod
    def run(cls, database, distribute_scheme):
        with Distributer(distribute_scheme) as distributer:
            saver = cls(database)

            def callback(data):
                user_id = data[keys.metadata][keys.user_id]
                topic = data[keys.metadata][keys.topic]
                if topic == keys.user:
                    saver.save_user(user_id, data[keys.data])
                else:
                    datetime = data[keys.metadata][keys.datetime]
                    saver.save_snapshot_topic(
                        topic, user_id, datetime, data[keys.data])

            distributer.subscribe(callback, 'user', 'parsed.*',
                                  subscriber_group=cls.group)

    # def connect(self):
    #     if hasattr(self.driver, 'connect'):
    #         return self.driver.connect()

    # def close(self):
    #     if hasattr(self.driver, 'close'):
    #         return self.driver.close()

    # def __enter__(self):
    #     self.connect()
    #     return self

    # def __exit__(self, exception, error, traceback):
    #     self.close()
