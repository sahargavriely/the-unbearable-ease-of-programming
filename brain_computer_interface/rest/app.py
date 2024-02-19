import functools
from http import HTTPStatus
import inspect
from pathlib import Path

import flask

from ..utils import (
    keys,
    setup_logging
)


logger = setup_logging(__name__)


class App:

    def __init__(self, **context):
        self.context = context
        self._resources = list()
        self._error_resources = list()
        self._app = flask.Flask(__name__)

    def __call__(self, *args, **kwds):
        return self._app(*args, **kwds)

    def register_collected_resources(self):
        for path, function in self._resources:
            handler = self._wrap_resource(function)
            self._app.route(path)(handler)
        for status_code, *indetifiyers in self._error_resources:
            handler = functools.partial(_handle_error, status_code)
            self._app.register_error_handler(status_code, handler)
            for indetifiyer in indetifiyers:
                self._app.register_error_handler(indetifiyer, handler)

    def resource(self, path):
        return self._collect(path)

    def error_resource(self, status_code, *indetifiyers):
        self._error_resources.append((status_code, *indetifiyers))

    def _collect(self, path):
        def decorator(function):
            self._resources.append((path, function))
            return function
        return decorator

    def _wrap_resource(self, function):
        @functools.wraps(function)
        def handler(**kwargs):
            req = flask.request
            logger.info('Got request %s %s from %s',
                        *_request_method_rule_ip(req))
            result = _inject(function, request=req, **self.context, **kwargs)
            data, status_code, headers = _parse_resource_result(result)
            if isinstance(data, Path):
                return flask.send_file(data), status_code, headers
            return flask.jsonify(data), status_code, headers
        return handler


def _handle_error(status_code, error):
    logger.error('%s: While handling %s %s from %s an error occurred %s',
                 status_code, *_request_method_rule_ip(flask.request), error)
    return flask.jsonify({keys.error: str(error)}), status_code


def _parse_resource_result(result):
    status_code, headers = HTTPStatus.OK, dict()
    return result, status_code, headers


def _inject(function, **options):
    spec = inspect.getfullargspec(function)
    kwargs = {}
    for key, value in options.items():
        if key in spec.args:
            kwargs[key] = value
    return function(**kwargs)


def _request_method_rule_ip(request: flask.Request):
    method = request.method
    rule = request.url_rule and request.url_rule.rule
    ip = _ip_extractor(request)
    return method, rule, ip


def _ip_extractor(request):
    return request.environ.get('HTTP_X_FORWARDED_FOR',
                               request.environ['REMOTE_ADDR'])
