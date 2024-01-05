import importlib
import inspect
import pathlib

import furl

from ..utils import setup_logging


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

    def publish_raw_snapshot(self, raw_snapshot):
        return self.driver.publish_raw_snapshot(raw_snapshot)

    def subscribe(self, callback):
        return self.driver.subscribe(callback)

    def connect(self):
        if hasattr(self.driver, 'connect'):
            return self.driver.connect()

    def close(self):
        if hasattr(self.driver, 'close'):
            return self.driver.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
