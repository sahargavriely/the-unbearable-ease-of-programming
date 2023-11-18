import inspect


class Parser:
    def __init__(self, **global_context):
        self.global_context = global_context
        self.parsers = dict()

    def __call__(self, parser_name):
        def decorator(function):
            if inspect.isclass(function):
                function = function().parse
            self.parsers[parser_name] = function
            return function
        return decorator

    def parse(self, cur_user_dir, snapshot, **local_context):
        for parser in self.parsers.values():
            _inject(parser, cur_user_dir=cur_user_dir, snapshot=snapshot,
                    **local_context, **self.global_context)


def _inject(function, **options):
    spec = inspect.getfullargspec(function)
    kwargs = {}
    for key, value in options.items():
        if key in spec.args:
            kwargs[key] = value
    return function(**kwargs)
