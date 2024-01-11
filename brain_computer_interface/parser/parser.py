import datetime as dt
import inspect
import functools

from . import parsers
from ..distributer import Distributer
from ..utils import SHARED_DIR, DISTRIBUTE_SCHEME


CLASS_PREDICT = 'Parser'
FUNC_PREDICT = 'parse_'


def run_parser(name, shared_dir=SHARED_DIR,
               distribute_scheme=DISTRIBUTE_SCHEME, group=False):
    parser = _get_parser(name)
    sub_topic = f'raw.{name}'
    if hasattr(parser, 'subscribe'):
        sub_topic = getattr(parser, 'subscribe')
    pub_topic = f'parsed.{name}'
    if hasattr(parser, 'publish'):
        pub_topic = getattr(parser, 'publish')

    def callback(data):
        with Distributer(distribute_scheme) as distributer:
            distributer.publish(parse(name, data, shared_dir), pub_topic)

    with Distributer(distribute_scheme) as distributer:
        group = name if group else ''
        distributer.subscribe(callback, sub_topic, group)


def parse(name, data, shared_dir=SHARED_DIR):
    parser = functools.partial(_get_parser(name), data['data'])
    img_dir = _get_img_dir(data['metadata'], shared_dir)
    return _inject(parser, img_dir=img_dir)


def _get_parser(name):
    parsers = _collect_parsers()
    if name not in parsers:
        raise ValueError(
            f'We want looking everywhere but did not find {name!r} parser')
    return parsers[name]


def _collect_parsers():
    parsers_ = dict()
    classes = inspect.getmembers(parsers, _class_predict)
    functions = inspect.getmembers(parsers, _function_predict)
    parsers_.update({_get_class_name(c): c().parse for _, c in classes})
    parsers_.update({_get_function_name(f): f for _, f in functions})
    return parsers_


def _class_predict(cls):
    return inspect.isclass(cls) and cls.__name__.endswith(CLASS_PREDICT)


def _function_predict(fun):
    return inspect.isfunction(fun) and fun.__name__.startswith(FUNC_PREDICT)


def _get_class_name(cls):
    if hasattr(cls, 'name'):
        return getattr(cls, 'name')
    cap_name = cls.__name__.removesuffix(CLASS_PREDICT)
    return ''.join(' ' + c.lower() if c.isupper() else c
                   for c in cap_name).strip().replace(' ', '_')


def _get_function_name(fun):
    if hasattr(fun, 'name'):
        return getattr(fun, 'name')
    return fun.__name__.removeprefix(FUNC_PREDICT)


def _get_img_dir(metadata, shared_dir):
    datetime = dt.datetime.fromtimestamp(metadata['datetime'] / 1000)
    user_id = str(metadata['user_id'])
    img_dir = shared_dir / user_id / f'{datetime:%F_%H-%M-%S-%f}'
    img_dir.mkdir(parents=True, exist_ok=True)
    return img_dir


def _inject(function, **options):
    spec = inspect.getfullargspec(function)
    kwargs = {}
    for key, value in options.items():
        if key in spec.args:
            kwargs[key] = value
    return function(**kwargs)
