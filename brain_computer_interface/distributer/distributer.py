import importlib
import inspect
import pathlib

from ..utils import setup_logging


logger = setup_logging(__name__)
distributors = dict()


def load_drivers():
    '''
    Loading drivers under drivers directory, relative to here.
    '''
    drivers = pathlib.Path(__file__).parent / 'drivers'
    for file in drivers.iterdir():
        if file.suffix != '.py' or file.name.startswith('_'):
            logger.info('did not load %s', file.name)
            continue
        logger.info('loading module driver %s', file.name)
        driver_import = f'.{drivers.name}.{file.stem}'
        driver = importlib.import_module(driver_import, __package__)
        for _, obj in inspect.getmembers(driver, inspect.isclass):
            if hasattr(obj, 'scheme'):
                logger.info('loading driver %s', obj.__name__)
                distributors[getattr(obj, 'scheme')] = obj


load_drivers()
