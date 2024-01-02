import inspect
from pathlib import Path

from . import parsers
from ..message import Snapshot


class Parser:
    def __init__(self, **global_context):
        self.global_context = global_context
        self.parsers = dict()
        self.collect_parsers()

    def collect_parsers(self):
        classes = inspect.getmembers(parsers, class_predict)
        functions = inspect.getmembers(parsers, function_predict)
        self.parsers.update({f.field: f for _, f in functions})
        self.parsers.update({c.field: c().parse for _, c in classes})

    def __call__(self, parser_name):
        def decorator(obj):
            if inspect.isclass(obj):
                obj = obj().parse
            self.parsers[parser_name] = obj
            return obj
        return decorator

    def parse(self, cur_user_dir: Path, snapshot: Snapshot, **local_context):
        cur_user_dir.mkdir(parents=True, exist_ok=True)
        for parser in self.parsers.values():
            _inject(parser, cur_user_dir=cur_user_dir, snapshot=snapshot,
                    **local_context, **self.global_context)


def class_predict(obj):
    return hasattr(obj, 'field') \
        and inspect.isclass(obj) \
        and obj.__name__.endswith('Parser')


def function_predict(obj):
    return hasattr(obj, 'field') \
        and inspect.isfunction(obj) \
        and obj.__name__.startswith('parse_')


def _inject(function, **options):
    spec = inspect.getfullargspec(function)
    kwargs = {}
    for key, value in options.items():
        if key in spec.args:
            kwargs[key] = value
    return function(**kwargs)
