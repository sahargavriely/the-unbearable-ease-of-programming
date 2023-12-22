import gzip
import struct

from ..reader import collect_driver
from ....protocol import (
    Snapshot,
    User,
)


drivers = dict()

length_format = '<I'


@collect_driver('gz')
class Compressed:
    def __init__(self, path: str):
        self.path = path

    def open(self) -> gzip.GzipFile:
        return gzip.open(self.path, 'rb')

    def read_user(self, file: gzip.GzipFile) -> User:
        length, = _read_and_decode(file, length_format)
        encoded_user = file.read(length)
        return User.from_bytes(encoded_user)

    def read_snapshot(self, file: gzip.GzipFile) -> Snapshot:
        length, = _read_and_decode(file, length_format)
        encoded_snapshot = file.read(length)
        return Snapshot.from_bytes(encoded_snapshot)


def _read_and_decode(file: gzip.GzipFile, format: str):
    size = struct.calcsize(format)
    return struct.unpack(format, file.read(size))
