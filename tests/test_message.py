import pytest

from brain_computer_interface.message import (
    Config,
    CONFIG_OPTIONS,
    Snapshot,
    User,
)
from brain_computer_interface.message.protobuf_wrapper import ProtobufWrapper


def test_config(config: Config):
    assert repr(config) == \
        repr(Config.from_bytes(config.serialize()))
    for con in config.config:
        assert con in config
    assert config == Config.from_json(config.jsonify())


def test_snapshot(snapshot: Snapshot):
    assert repr(snapshot) == \
        repr(Snapshot.from_bytes(snapshot.serialize()))
    assert snapshot == Snapshot.from_json(snapshot.jsonify())
    for con in CONFIG_OPTIONS:
        snapshot.set_default(con)


def test_user(user: User):
    assert repr(user) == \
        repr(User.from_bytes(user.serialize()))
    assert user == User.from_json(user.jsonify())


def test_missing_pb_type():
    with pytest.raises(AttributeError,
                       match=r'Missing _protobuf_type attribute'):
        ProtobufWrapper.from_bytes(b'')
