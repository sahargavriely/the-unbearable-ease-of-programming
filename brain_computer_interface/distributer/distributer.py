import contextlib

import furl

from ..message import CONFIG_OPTIONS
from ..utils import get_driver, keys, setup_logging


logger = setup_logging(__name__)


class Distributer:
    def __init__(self, url: str):
        logger.info('initiating distributer for url %s', url)
        url_ = furl.furl(url)
        self.driver = get_driver(
            __file__, __package__, 'scheme', url_.scheme)(url_)

    def connect(self):
        if hasattr(self.driver, 'connect'):
            return self.driver.connect()

    def close(self):
        if hasattr(self.driver, 'close'):
            return self.driver.close()

    def publish_raw_snapshot(self, data):
        metadata = dict(user_id=data[keys.user][keys.id],
                        datetime=data[keys.snapshot][keys.datetime])
        for topic in CONFIG_OPTIONS:
            metadata['topic'] = topic
            raw_topic_data = dict(metadata=metadata,
                                  data=data[keys.snapshot][topic])
            self.publish(raw_topic_data, f'raw.{topic}')

    def publish_parsed_topic(self, parsed_topic_data, topic):
        return self.publish(parsed_topic_data, f'parsed.{topic}')

    def publish(self, data, topic):
        logger.info('publishing to %s', topic)
        return self.driver.publish(data, topic)

    def subscribe_parsed_topic(self, callback, topic, subscriber_group=''):
        self.subscribe(callback, f'parsed.{topic}',
                       subscriber_group=subscriber_group)

    def subscribe_raw_topic(self, callback, topic, subscriber_group=''):
        self.subscribe(callback, f'raw.{topic}',
                       subscriber_group=subscriber_group)

    def subscribe(self, callback, *topics, subscriber_group=''):
        logger.info('subscribing to %s part of group %s',
                    topics, subscriber_group)
        with contextlib.suppress(Exception):
            self.driver.subscribe(callback, *topics,
                                  subscriber_group=subscriber_group)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
