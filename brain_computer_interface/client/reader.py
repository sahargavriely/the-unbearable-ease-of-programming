from datetime import datetime
from io import BufferedReader
from pathlib import Path
import struct

from PIL import Image

from ..utils import (
    Snapshot,
    User,
)


id_format = '<Q'
name_len_format = '<I'
b_day_format = '<I'
timestamp_format = '<Q'
translation_format = '<ddd'
rotation_format = '<dddd'
height_format = '<I'
width_format = '<I'
pixel_format = '<f'
feelings_format = '<ffff'


class Reader:
    def __init__(self, path: Path):
        self.path = path
        self.file_pointer = 0
        self.read_user()

    def read_user(self):
        with self as file:
            id, = read_and_decode(file, id_format)
            name_len, = read_and_decode(file, name_len_format)
            name = file.read(name_len).decode()
            b_day = datetime.fromtimestamp(read_and_decode(file, b_day_format)[0])
            gender = file.read(1).decode()
        self.user = User(id, name, b_day, gender)

    def __iter__(self):
        return self

    def __next__(self) -> Snapshot:
        with self as file:
            if file.tell() == self.path.stat().st_size:
                raise StopIteration('No more snapshots to read')
            timestamp = datetime.fromtimestamp(read_and_decode(file, timestamp_format)[0] / 1000)
            translation = read_and_decode(file, translation_format)
            rotation = read_and_decode(file, rotation_format)
            color_image = read_and_decode_image(file, 'RGB')
            depth_image = read_and_decode_image(file, 'F')
            feelings = read_and_decode(file, feelings_format)
        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)

    def __enter__(self) -> BufferedReader:
        self.file = self.path.open('rb')
        self.file.seek(self.file_pointer)
        return self.file

    def __exit__(self, exception, error, traceback):
        if self.file:
            self.file_pointer = self.file.tell()
            self.file.close()
            del self.file


def read_and_decode(file: BufferedReader, format: str):
    size = struct.calcsize(format)
    return struct.unpack(format, file.read(size))


def read_and_decode_image(file: BufferedReader, mode: str):
    height, = read_and_decode(file, height_format)
    width, = read_and_decode(file, width_format)
    image_data = b''
    if mode == 'RGB':
        image_data = list()
        for _ in range(height * width):
            b = file.read(1)
            g = file.read(1)
            r = file.read(1)
            image_data.append(r)
            image_data.append(g)
            image_data.append(b)
        image_data = b''.join(image_data)
    elif mode == 'F':
        image_data = file.read(height * width * struct.calcsize(pixel_format))
    return Image.frombytes(mode, (width, height), image_data, 'raw')
