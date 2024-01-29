import functools
from http import HTTPStatus
import inspect
from pathlib import Path

import flask

from ..database import Database
from ..utils import (
    DATABASE_SCHEME,
    LISTEN_HOST,
    keys,
    REST_SERVER_PORT,
    setup_logging
)

import logging
logger = setup_logging(__name__, logging.INFO)
_resources = list()


def run_rest_server(host: str = LISTEN_HOST, port: int = REST_SERVER_PORT,
                    database_scheme: str = DATABASE_SCHEME):
    app = flask.Flask(__name__)
    db = Database(database_scheme)

    def _wrap_resource(function):
        @functools.wraps(function)
        def handler(**kwargs):
            logger.info('Got request %s %s from %s',
                        *_request_method_rule_ip(flask.request))
            result = _inject(function, request=flask.request, db=db, **kwargs)
            data, status_code, headers = _parse_resource_result(result)
            if isinstance(data, Path):
                return flask.send_file(data), status_code, headers
            return flask.jsonify(data), status_code, headers
        return handler

    for path, function in _resources:
        handler = _wrap_resource(function)
        app.route(path)(handler)
    app.register_error_handler(HTTPStatus.NOT_FOUND, _handle_not_found)
    app.register_error_handler(HTTPStatus.METHOD_NOT_ALLOWED,
                               _handle_method_not_allowed)
    app.register_error_handler(ValueError, _handle_bad_request)
    app.register_error_handler(Exception, _handle_server_error)

    app.run(host=host, port=port)


def collect_resource(path):
    def decorator(function):
        _resources.append((path, function))
        return function
    return decorator


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


@collect_resource('/users')
def users(db: Database):
    return db.get_users()


@collect_resource('/users/<int:id>')
def user(id, db: Database):
    return db.get_user(id)


@collect_resource('/users/<int:id>/snapshots')
def user_snapshots(id, db: Database):
    return db.get_user_snapshots(id)


@collect_resource('/users/<int:id>/snapshots/<int:datetime>')
def user_snapshot(id, datetime, db: Database):
    return db.get_user_snapshot(id, datetime)


@collect_resource('/users/<int:id>/snapshots/<int:datetime>/<string:topic>')
def user_snapshot_topic(id, datetime, topic, db: Database):
    return db.get_user_snapshot_topic(id, datetime, topic)


@collect_resource(
    '/users/<int:id>/snapshots/<int:datetime>/<string:topic>/data')
def user_snapshot_topic_data(id, datetime, topic, db: Database):
    topic_content = db.get_user_snapshot_topic(id, datetime, topic)
    if keys.data not in topic_content:
        raise ValueError(f'Topic {topic!r} does not have data')
    return Path(topic_content[keys.data])


def _handle_bad_request(error):
    logger.error('While handling %s %s from %s an error (400) occurred %s',
                 *_request_method_rule_ip(flask.request), error)
    bad_request_error = {keys.error: str(error)}
    return flask.jsonify(bad_request_error), HTTPStatus.BAD_REQUEST


def _handle_not_found(error):
    logger.error('While handling %s %s from %s an error (404) occurred %s',
                 *_request_method_rule_ip(flask.request), error)
    not_found_error = {keys.error: str(error)}
    return flask.jsonify(not_found_error), HTTPStatus.NOT_FOUND


def _handle_method_not_allowed(error):
    logger.error('While handling %s %s from %s an error (405) occurred %s',
                 *_request_method_rule_ip(flask.request), error)
    method_not_allowed = {keys.error: str(error)}
    return flask.jsonify(method_not_allowed), HTTPStatus.METHOD_NOT_ALLOWED


def _handle_server_error(error):
    logger.error('While handling %s %s from %s an error (500) occurred %s',
                 *_request_method_rule_ip(flask.request), error)
    server_error_error = {keys.error: str(error)}
    return flask.jsonify(server_error_error), HTTPStatus.INTERNAL_SERVER_ERROR


def _request_method_rule_ip(request: flask.Request):
    method = request.method
    rule = request.url_rule and request.url_rule.rule
    ip = _ip_extractor(request)
    return method, rule, ip


def _ip_extractor(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    return request.environ['HTTP_X_FORWARDED_FOR']
