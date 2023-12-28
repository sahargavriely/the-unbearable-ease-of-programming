import inspect
import json
import pathlib

import furl

from ..utils import setup_logging


logger = setup_logging(__name__)
schemes = dict()


def collect_scheme(scheme):

    def decorator(func):
        logger.info('collecting publish scheme %s', scheme)
        schemes[scheme] = func
        return func

    if inspect.isfunction(scheme):
        func, scheme = scheme, scheme.__name__
        return decorator(func)
    return decorator


@collect_scheme
def file(url: furl.furl, data):
    path = pathlib.Path(str(url.path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as f:
        json.dump(data, f)
