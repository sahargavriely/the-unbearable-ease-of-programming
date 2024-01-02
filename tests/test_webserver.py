import datetime as dt
from http import HTTPStatus

import requests
import pytest


@pytest.fixture
def user_dir(conf):
    conf.SHARED_DIR.mkdir()
    user_dir = conf.SHARED_DIR / str(conf.USER_20)
    user_dir.mkdir()
    datetime = dt.datetime.fromtimestamp(conf.TIMESTAMP_20)
    thought_file = user_dir / f'{datetime:%F_%H-%M-%S}.txt'
    thought_file.write_text(conf.THOUGHT_20)
    yield user_dir


def test_index(webserver, conf):
    response = requests.get(conf.WEBSERVER_URL)
    assert response.status_code == HTTPStatus.OK
    assert 'Brain Computer Interface' in response.text


def test_user(webserver, conf, user_dir):
    response = requests.get(conf.WEBSERVER_URL)
    assert response.status_code == HTTPStatus.OK
    assert f'user {user_dir.name}' in response.text
    assert f'users/{user_dir.name}' in response.text
    response = requests.get(f'{conf.WEBSERVER_URL}/users/{user_dir.name}')
    assert f'User {user_dir.name}' in response.text
    datetime = dt.datetime.fromtimestamp(conf.TIMESTAMP_20)
    assert f'{datetime:%F %T}' in response.text
    assert conf.THOUGHT_20 in response.text


def test_user_not_found(webserver, conf):
    user_id = 69
    response = requests.get(f'{conf.WEBSERVER_URL}/users/{user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert f'We want looking everywhere but did not found user {user_id}' \
        in response.text
