from brain_computer_interface import upload_thought

from utils import _assert_now


def test_connection(conf, get_message):
    args = conf.USER_20, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    message = get_message()
    assert message


def test_user_id(conf, get_message):
    args = conf.USER_20, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    user_id, _, _ = get_message()
    assert user_id == conf.USER_20
    args = conf.USER_22, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    user_id, _, _ = get_message()
    assert user_id == conf.USER_22


def test_thought(conf, get_message):
    args = conf.USER_20, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    _, _, thought = get_message()
    assert thought == conf.THOUGHT_20
    args = conf.USER_20, conf.THOUGHT_22, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    _, _, thought = get_message()
    assert thought == conf.THOUGHT_22


def test_timestamp(conf, get_message):
    args = conf.USER_20, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    _, timestamp, _ = get_message()
    _assert_now(timestamp)
    args = conf.USER_22, conf.THOUGHT_22, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    _, timestamp, _ = get_message()
    _assert_now(timestamp)
