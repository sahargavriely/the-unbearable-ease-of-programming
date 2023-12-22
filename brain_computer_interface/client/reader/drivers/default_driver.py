from io import BufferedReader
import struct

from ..reader import collect_driver
from ....protocol import (
    ColorImage,
    DepthImage,
    Feelings,
    Pose,
    Rotation,
    Snapshot,
    Translation,
    User,
)


id_format = '<Q'
name_len_format = '<I'
birthday_format = '<I'
datetime_format = '<Q'
translation_format = '<ddd'
rotation_format = '<dddd'
height_format = '<I'
width_format = '<I'
pixel_format = '<f'
feelings_format = '<ffff'


@collect_driver
class Default:
    def __init__(self, path: str):
        self.path = path

    def open(self):
        return open(self.path, 'rb')

    def read_user(self, file: BufferedReader) -> User:
        id, = read_and_decode(file, id_format)
        name_len, = read_and_decode(file, name_len_format)
        name = file.read(name_len).decode()
        birthday, = read_and_decode(file, birthday_format)
        g = file.read(1).decode()
        gender = 0 if g == 'm' else 1 if g == 'f' else 2
        return User(id, name, birthday, gender)

    def read_snapshot(self, file: BufferedReader) -> Snapshot:
        datetime, = read_and_decode(file, datetime_format)
        pose = Pose(Translation(*read_and_decode(file, translation_format)),
                    Rotation(*read_and_decode(file, rotation_format)))
        color_image = ColorImage(*read_and_decode_color_image(file))
        depth_image = DepthImage(*read_and_decode_depth_image(file))
        feelings = Feelings(*read_and_decode(file, feelings_format))
        return Snapshot(
            datetime,
            pose,
            color_image,
            depth_image,
            feelings
        )


def read_and_decode(file: BufferedReader, format: str):
    size = struct.calcsize(format)
    return struct.unpack(format, file.read(size))


def read_and_decode_height_and_width(file: BufferedReader) -> tuple[int, int]:
    height, = read_and_decode(file, height_format)
    width, = read_and_decode(file, width_format)
    return width, height


def read_and_decode_depth_image(
        file: BufferedReader) -> tuple[int, int, list[float]]:
    width, height = read_and_decode_height_and_width(file)
    data = list()
    for _ in range(height * width):
        pixel, = read_and_decode(file, pixel_format)
        data.append(pixel)
    return width, height, data


def read_and_decode_color_image(
        file: BufferedReader) -> tuple[int, int, bytes]:
    width, height = read_and_decode_height_and_width(file)
    data = list()
    for _ in range(height * width):
        b = file.read(1)
        g = file.read(1)
        r = file.read(1)
        data.append(r)
        data.append(g)
        data.append(b)
    data = b''.join(data)
    return width, height, data
