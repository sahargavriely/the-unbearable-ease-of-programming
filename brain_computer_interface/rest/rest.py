from http import HTTPStatus
from pathlib import Path

from .app import App
from .wsgi import StandaloneApplication
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
    db = Database(database_scheme)
    app = App(host, port, db=db)

    for path, function in _resources:
        app.resource(path)(function)
    app.error_resource(HTTPStatus.NOT_FOUND)
    app.error_resource(HTTPStatus.METHOD_NOT_ALLOWED)
    app.error_resource(HTTPStatus.BAD_REQUEST, ValueError)
    app.error_resource(HTTPStatus.INTERNAL_SERVER_ERROR, Exception)
    app.register_collected_resources()

    options = {
        'bind': f'{host}:{port}',
        'max_requests': 200,
        'max_requests_jitter': 20,
    }
    StandaloneApplication(app, options).run()


def collect_resource(path):
    def decorator(function):
        _resources.append((path, function))
        return function
    return decorator


@collect_resource('/error')
def error():
    raise Exception('Server error')


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
