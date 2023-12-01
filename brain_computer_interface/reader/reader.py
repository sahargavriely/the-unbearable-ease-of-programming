import os

from .drivers import drivers
from ..protocol import Snapshot


def find_driver(path: str):
    extension = path.split('.')[-1]
    driver = drivers.get(extension, drivers.get('default'))
    return driver(path)


class Reader:
    def __init__(self, path: str):
        self.driver = find_driver(path)
        self.file_pointer = 0
        with self as file:
            self.user = self.driver.read_user(file)

    def __iter__(self):
        return self

    def __next__(self) -> Snapshot:
        with self as file:
            if not file.peek(1):
                raise StopIteration('No more snapshots to read')
            return self.driver.read_snapshot(file)

    def __enter__(self):
        self.file = self.driver.open()
        self.file.seek(self.file_pointer)
        return self.file

    def __exit__(self, exception, error, traceback):
        if self.file:
            self.file_pointer = self.file.tell()
            self.file.close()
            del self.file
