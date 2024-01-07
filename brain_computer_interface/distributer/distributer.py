import importlib
import inspect
import pathlib

import furl

from ..message import CONFIG_OPTIONS
from ..utils import keys, setup_logging


logger = setup_logging(__name__)


def get_driver(scheme):
    '''
    Loading drivers under drivers directory, relative to here.
    '''
    drivers = pathlib.Path(__file__).parent / 'drivers'
    for file in drivers.iterdir():
        if file.suffix != '.py' or file.name.startswith('_'):
            logger.info('did not load %s', file.name)
            continue
        logger.info('loading module %s for distributer driver', file.name)
        driver_import = f'.{drivers.name}.{file.stem}'
        driver = importlib.import_module(driver_import, __package__)
        for _, obj in inspect.getmembers(driver, inspect.isclass):
            if hasattr(obj, 'scheme') and getattr(obj, 'scheme') == scheme:
                logger.info(
                    'located and loading distributer driver %s', obj.__name__)
                return obj
    err_msg = f'Could not locate distributer driver scheme {scheme!r}'
    logger.error(err_msg)
    raise ValueError(err_msg)


class Distributer:
    def __init__(self, url: str):
        self.url = furl.furl(url)
        self.driver = get_driver(self.url.scheme)(self.url)

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
            raw_topic_data = dict(metadata=metadata,
                                  data=data[keys.snapshot][topic])
            self.publish(raw_topic_data, f'raw.{topic}')

    def publish_parsed_topic(self, parsed_topic_data, topic):
        return self.publish(parsed_topic_data, f'parsed.{topic}')

    def publish(self, data, topic):
        return self.driver.publish(data, topic)

    def subscribe_parsed_topic(self, callback, topic, subscriber_group=''):
        return self.subscribe(callback, f'parsed.{topic}', subscriber_group)

    def subscribe_raw_topic(self, callback, topic, subscriber_group=''):
        return self.subscribe(callback, f'raw.{topic}', subscriber_group)

    def subscribe(self, callback, topic, subscriber_group=''):
        return self.driver.subscribe(callback, topic, subscriber_group)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
