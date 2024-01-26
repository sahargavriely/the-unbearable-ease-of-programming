import datetime as dt
from http import HTTPStatus

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys


def test_not_found(rest_server, client):
    response = client.get('/not-existing-api')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert keys.error in response.json()
    assert response.json()[keys.error] == 'API request does not exists'


def test_method_not_allowed(rest_server, client):
    response = client.post('/users')
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert keys.error in response.json()
    assert response.json()[keys.error] == 'Method not allowed'


def test_user(rest_server, client, database, user):
    response = client.get('/users')
    _assert_ok(response, list())
    user_id = user.id
    response = client.get(f'/users/{user_id}')
    _assert_bad_request(response, f'User id {user_id!r} does not exists')
    database.save_user(user_id, user.jsonify())
    response = client.get('/users')
    _assert_ok(response, [user_id])
    response = client.get(f'/users/{user_id}')
    _assert_ok(response, user.jsonify())


def test_snapshot(rest_server, client, database, user, parsed_data, snapshot):
    user_id = user.id
    datetime = snapshot.datetime
    datetime_ = dt.datetime.fromtimestamp(datetime / 1000)
    response = client.get(f'/users/{user_id}/snapshots')
    _assert_ok(response, list())
    response = client.get(f'/users/{user_id}/snapshots/{datetime}')
    _assert_bad_request(response, f'User id {user_id!r} does not have '
                                  f'snapshot from {datetime_:%F_%H-%M-%S-%f}')
    topic = CONFIG_OPTIONS[0]
    response = client.get(f'/users/{user_id}/snapshots/{datetime}/{topic}')
    _assert_bad_request(response, f'User id {user_id!r} snapshot from '
                                  f'{datetime_:%F_%H-%M-%S-%f} does not '
                                  f'have {topic!r}')
    for topic in CONFIG_OPTIONS:
        database.save_snapshot_topic(
            user_id, datetime, topic, parsed_data[topic][keys.data])
    response = client.get(f'/users/{user_id}/snapshots')
    _assert_ok(response, [datetime])
    saved_snap = dict(datetime=datetime)
    for topic in CONFIG_OPTIONS:
        saved_snap[topic] = parsed_data[topic][keys.data]
        response = client.get(f'/users/{user_id}/snapshots/{datetime}/{topic}')
        _assert_ok(response, parsed_data[topic][keys.data])
    response = client.get(f'/users/{user_id}/snapshots/{datetime}')
    _assert_ok(response, saved_snap)


def _assert_ok(response, expected_response):
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


def _assert_bad_request(response, expected_response):
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert keys.error in response.json()
    assert response.json()[keys.error] == expected_response
