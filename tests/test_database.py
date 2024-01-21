import datetime as dt

import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys
from brain_computer_interface.database import Database


@pytest.fixture(params=['DATABASE', 'POSTGRES_SCHEME'])
def database(conf, request):
    db = Database(conf.get(request.param))
    yield db
    db.drop_db()


def test_user(database, user):
    assert database.get_users() == list()
    user_id = user.id
    with pytest.raises(ValueError, match=
                       f'User id {user_id!r} does not exists'):
        database.get_user(user_id)
    database.save_user(user_id, user.jsonify())
    assert database.get_users() == [user_id]
    assert database.get_user(user_id) == user.jsonify()


def test_snapshot(database, user, parsed_data, snapshot):
    user_id = user.id
    datetime = snapshot.datetime
    datetime_ = dt.datetime.fromtimestamp(datetime / 1000)
    with pytest.raises(ValueError, match=
                       f'User id {user_id!r} does not have '
                       f'snapshot from {datetime_:%F_%H-%M-%S-%f}'):
        database.get_user_snapshot(user_id, datetime)
    topic = CONFIG_OPTIONS[0]
    with pytest.raises(ValueError, match=
                       f'User id {user_id!r} snapshot from '
                       f'{datetime_:%F_%H-%M-%S-%f} does not '
                       f'have {topic!r}'):
        database.get_user_snapshot_topic(user_id, datetime, topic)
    assert database.get_user_snapshots(user_id) == list()
    for topic in CONFIG_OPTIONS:
        database.save_snapshot_topic(
            user_id, datetime, topic, parsed_data[topic][keys.data])
    assert database.get_user_snapshots(user_id) == [datetime]
    saved_snap = database.get_user_snapshot(user_id, datetime)
    for topic in CONFIG_OPTIONS:
        assert saved_snap[topic] == parsed_data[topic][keys.data]
        data = database.get_user_snapshot_topic(user_id, datetime, topic)
        assert data == parsed_data[topic][keys.data]
