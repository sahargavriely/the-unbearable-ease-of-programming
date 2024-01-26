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
)


_resources = list()


def run_rest_server(host: str = LISTEN_HOST, port: int = REST_SERVER_PORT,
                    database_scheme: str = DATABASE_SCHEME):
    app = flask.Flask(__name__)
    db = Database(database_scheme)

    def _wrap_resource(function):
        @functools.wraps(function)
        def handler(*args):
            result = _inject(function, *args, request=flask.request, db=db)
            data, status_code, headers = _parse_resource_result(result)
            if isinstance(data, Path):
                return flask.send_file(data), status_code, headers
            return flask.jsonify(data), status_code, headers
        return handler

    # from werkzeug.routing import PathConverter
    # class NotAPIConvertor(PathConverter):
    #     regex = r'^(?!api\/.*$).*$'
    # class APIConvertor(PathConverter):
    #     regex = r'api\/.*$'
    # app.url_map.converters['does_not_start_with_api'] = NotAPIConvertor
    # app.url_map.converters['start_with_api'] = APIConvertor
    # app.route('/<does_not_start_with_api:path>')(handler)
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


def _inject(function, *args, **options):
    spec = inspect.getfullargspec(function)
    kwargs = {}
    for key, value in options.items():
        if key in spec.args:
            kwargs[key] = value
    return function(*args, **kwargs)


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
    topic = db.get_user_snapshot_topic(id, datetime, topic)
    if keys.data not in topic:
        raise ValueError(f'Topic {topic!r} does not have data')
    return Path(topic[keys.data])


def _handle_bad_request(error):
    bad_request_error = {'error': str(error)}
    return flask.jsonify(bad_request_error), HTTPStatus.BAD_REQUEST


def _handle_not_found(error):
    not_found_error = {'error': 'API request not found'}
    return flask.jsonify(not_found_error), HTTPStatus.NOT_FOUND


def _handle_method_not_allowed(error):
    method_not_allowed = {'error': 'method not allowed'}
    return flask.jsonify(method_not_allowed), HTTPStatus.METHOD_NOT_ALLOWED


def _handle_server_error(error):
    server_error_error = {'error': str(error)}
    return flask.jsonify(server_error_error), HTTPStatus.INTERNAL_SERVER_ERROR
