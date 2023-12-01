from brain_computer_interface.protocol import (
    Config,
    Snapshot,
    User,
)


def test_config(config: Config):
    assert repr(config) == \
        repr(Config.from_bytes(config.serialize()))
    for con in config.config:
        assert con in config


def test_snapshot(snapshot: Snapshot):
    assert repr(snapshot) == \
        repr(Snapshot.from_bytes(snapshot.serialize()))
    for con in Snapshot.config:
        snapshot.set_default(con)


def test_user(user: User):
    assert repr(user) == \
        repr(User.from_bytes(user.serialize()))
