from pathlib import Path

from brain_computer_interface import Reader

from brain_computer_interface.protocol import (
    Snapshot,
    User,
)


def test_read_mind_file(mind_file: Path, user: User, snapshot: Snapshot):
    reader = Reader(str(mind_file))
    assert reader.user.serialize() == user.serialize()
    for snap in reader:
        assert snap.serialize() == snapshot.serialize()


def test_read_compressed_mind_file(compressed_mind_file: Path, user: User, snapshot: Snapshot):
    reader = Reader(str(compressed_mind_file))
    assert reader.user.serialize() == user.serialize()
    for snap in reader:
        assert snap.serialize() == snapshot.serialize()
