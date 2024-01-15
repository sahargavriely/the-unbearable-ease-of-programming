from brain_computer_interface.message import CONFIG_OPTIONS


def test_user(saver, user):
    user_id = user.id
    saver.save_user(user_id, user.jsonify())
    assert saver.get_user(user_id) == user.jsonify()


def test_snapshots(saver, user, parsed_data, snapshot):
    user_id = user.id
    datetime = snapshot.datetime
    for topic in CONFIG_OPTIONS:
        saver.save_snapshot_topic(topic, user_id, datetime, parsed_data[topic])
    snapshot_dt, = saver.get_user_snapshots(user_id)
    assert snapshot_dt == datetime
    for topic in CONFIG_OPTIONS:
        data = parsed_data[topic]
        assert saver.get_snapshot_topic(topic, user_id, datetime) == data
