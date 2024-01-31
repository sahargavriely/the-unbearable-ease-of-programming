from pathlib import Path

from brain_computer_interface.client import (
    Reader,
    upload_mind,
    upload_thought,
)
from brain_computer_interface.message import (
    Snapshot,
    User,
)

from tests.client.utils import assert_now


def test_read_mind_file(default_mind_file: Path, user: User,
                        snapshot: Snapshot):
    reader = Reader(str(default_mind_file))
    assert reader.user.serialize() == user.serialize()
    for snap in reader:
        assert snap.serialize() == snapshot.serialize()


def test_read_protobuf_mind_file(protobuf_mind_file: Path, user: User,
                                 snapshot: Snapshot):
    reader = Reader(str(protobuf_mind_file))
    assert reader.user.serialize() == user.serialize()
    for snap in reader:
        assert repr(snap) == repr(snapshot)


def test_upload_mind(conf, default_mind_file, protobuf_mind_file, user,
                     snapshot, get_message):
    upload_mind(str(default_mind_file), conf.REQUEST_HOST, conf.SERVER_PORT)
    decoded_user, decoded_snapshots, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert repr(Snapshot.from_bytes(decoded_snapshots[0])) == repr(snapshot)

    upload_mind(str(protobuf_mind_file), conf.REQUEST_HOST, conf.SERVER_PORT)
    decoded_user, decoded_snapshots, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert repr(Snapshot.from_bytes(decoded_snapshots[0])) == repr(snapshot)


def test_upload_thought(conf, get_message):
    args = conf.USER_20, conf.THOUGHT_20, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_20
    assert_now(timestamp)
    assert thought == conf.THOUGHT_20

    args = conf.USER_22, conf.THOUGHT_22, conf.REQUEST_HOST, conf.SERVER_PORT
    upload_thought(*args)
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_22
    assert_now(timestamp)
    assert thought == conf.THOUGHT_22
