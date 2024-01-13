import importlib
import inspect
import pathlib

from .logging_setter import setup_logging


logger = setup_logging(__name__)


def get_driver(file, package, predict_key, predict):
    '''
    Loading drivers under drivers directory, relative to package.
    '''
    drivers = pathlib.Path(file).parent / 'drivers'
    for file in drivers.iterdir():
        if file.suffix != '.py' or file.name.startswith('_'):
            logger.info('did not load %s', file.name)
            continue
        logger.info('loading module %s', file.name)
        driver_import = f'.{drivers.name}.{file.stem}'
        driver = importlib.import_module(driver_import, package)
        for _, obj in inspect.getmembers(driver, inspect.isclass):
            if getattr(obj, predict_key, None) == predict:
                logger.info('located and loading driver %s', obj.__name__)
                return obj
    err_msg = f'Could not locate driver {predict_key} {predict!r}'
    logger.error(err_msg)
    raise ValueError(err_msg)
