from ..distributer import Distributer
from ..database import Database
from ..utils import keys, setup_logging


logger = setup_logging(__name__)


class Saver:
    group = 'saver'

    def __init__(self, url: str):
        logger.info('initiating saver for url %s', url)
        self.db = Database(url)

    def save_user(self, user_id, data):
        logger.info('saving to user id %s', user_id)
        return self.db.save_user(user_id, data)

    def save_snapshot_topic(self, user_id, datetime, topic, data):
        logger.info('saving %s of user id %s snapshot at datetime %s',
                    user_id, datetime, topic)
        return self.db.save_snapshot_topic(user_id, datetime, topic, data)

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
                        user_id, datetime, topic, data[keys.data])

            logger.info('initiating saver runner to handle parsed data')
            distributer.subscribe(callback, 'user', 'parsed.*',
                                  subscriber_group=cls.group)
