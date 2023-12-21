from brain_computer_interface.client import upload_mind, upload_thought

from utils import _assert_now


def test_upload_mind(conf, mind_file, compressed_mind_file, user, snapshot,
                     get_message):
    upload_mind(str(mind_file), conf.REQUEST_HOST, conf.SERVER_PORT)
    decoded_user, decoded_snapshot, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert decoded_snapshot == snapshot.serialize()

    upload_mind(str(compressed_mind_file), conf.REQUEST_HOST, conf.SERVER_PORT)
    decoded_user, decoded_snapshot, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert decoded_snapshot == snapshot.serialize()


def test_upload_thought(conf, get_message):
    args = conf.USER_20, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_20
    _assert_now(timestamp)
    assert thought == conf.THOUGHT_20

    args = conf.USER_22, conf.THOUGHT_22, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_22
    _assert_now(timestamp)
    assert thought == conf.THOUGHT_22
