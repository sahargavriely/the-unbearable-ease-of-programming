from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys


def test_user(saver, user):
    user_id = user.id
    saver.save_user(user_id, user.jsonify())
    assert saver.get_users() == [user_id]
    assert saver.get_user(user_id) == user.jsonify()


def test_snapshots(saver, user, parsed_data, snapshot):
    user_id = user.id
    datetime = snapshot.datetime
    for topic in CONFIG_OPTIONS:
        saver.save_snapshot_topic(
            topic, user_id, datetime, parsed_data[topic][keys.data])
    assert saver.get_user_snapshots(user_id) == [datetime]
    saved_snap = saver.get_user_snapshot(user_id, datetime)
    for topic in CONFIG_OPTIONS:
        assert saved_snap[topic] == parsed_data[topic][keys.data]
    for img in (keys.depth_image, keys.color_image):
        data = saver.get_user_snapshot_topic(img, user_id, datetime)
        with open(parsed_data[img][keys.data][keys.data], 'rb') as f:
            assert data == f.read()
