import inspect
import json


schemes = dict()


def collect_schemes(scheme):
    if inspect.isfunction(scheme):
        schemes[scheme.__name__] = scheme
        return scheme

    def decorator(func):
        schemes[scheme] = func
        return func
    return decorator


@collect_schemes('file')
def file(path, *data):
    with open(path, 'w') as f:
        json.dump(data, f)
