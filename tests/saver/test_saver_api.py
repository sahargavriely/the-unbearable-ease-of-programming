import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.saver import Saver
from brain_computer_interface.utils import keys


@pytest.fixture()
def saver(conf):
    yield Saver(conf.DATABASE_SCHEME)


def test_user(saver, database, user):
    user_id = user.id
    saver.save_user(user_id, user.jsonify())
    assert database.get_users() == [user_id]
    assert database.get_user(user_id) == user.jsonify()


def test_snapshots(saver, database, user, parsed_data, snapshot):
    user_id = user.id
    datetime = snapshot.datetime
    for topic in CONFIG_OPTIONS:
        saver.save_snapshot_topic(
            user_id, datetime, topic, parsed_data[topic][keys.data])
    assert database.get_user_snapshots(user_id) == [datetime]
    saved_snap = database.get_user_snapshot(user_id, datetime)
    for topic in CONFIG_OPTIONS:
        assert saved_snap[topic] == parsed_data[topic][keys.data]
        data = database.get_user_snapshot_topic(user_id, datetime, topic)
        assert data == parsed_data[topic][keys.data]
