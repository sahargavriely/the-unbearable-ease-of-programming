from pathlib import Path

from brain_computer_interface.client import Reader
from brain_computer_interface.protocol import (
    Snapshot,
    User,
)


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
        assert snap.serialize() == snapshot.serialize()
