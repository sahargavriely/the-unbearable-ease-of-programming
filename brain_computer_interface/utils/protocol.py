from datetime import datetime
from enum import Enum
import struct

from PIL import Image


TYPE_FORMAT = '<I'
TYPE_SIZE = struct.calcsize('<I')


class Types(Enum):
    MIND = 0
    THOUGHT = 1


########################################################
# note, definitions duplications from client/reader.py #
########################################################


id_format = '<Q'
name_len_format = '<I'
b_day_format = '<I'

list_size_format = '<I'
item_size_format = '<I'

timestamp_format = '<Q'
translation_format = '<ddd'
rotation_format = '<dddd'
height_format = '<I'
width_format = '<I'
pixel_format = '<f'
feelings_format = '<ffff'


class User:
    def __init__(self, id: int, name: str, b_day: datetime, gender: str):
        self.id = id
        self.name = name
        self.b_day = b_day
        self.gender = gender

    def serialize(self):
        return struct.pack(id_format, self.id) \
            + struct.pack(name_len_format, len(self.name.encode())) \
            + self.name.encode() \
            + struct.pack(b_day_format, int(self.b_day.timestamp())) \
            + self.gender.encode()

    @classmethod
    def from_bytes(cls, bytes: bytes):
        prefix = 0
        (id, ), prefix = cut_and_decode(bytes, prefix, id_format)
        (name_len, ), prefix = cut_and_decode(bytes, prefix, name_len_format)
        name = bytes[prefix: prefix + name_len].decode()
        prefix += name_len
        (b_day, ), prefix = cut_and_decode(bytes, prefix, b_day_format)
        b_day = datetime.fromtimestamp(b_day)
        gender = bytes[prefix: prefix + 1].decode()
        return User(id, name, b_day, gender)


class Config:
    def __init__(self, config: list[str]):
        self.config = config

    def __contains__(self, key):
        return key in self.config

    def serialize(self):
        data = [struct.pack(list_size_format, len(self.config))]
        for item in self.config:
            data.append(struct.pack(item_size_format, len(item.encode())))
            data.append(item.encode())
        return b''.join(data)

    @classmethod
    def from_bytes(cls, bytes: bytes):
        config = list()
        prefix = 0
        (list_size, ), prefix = cut_and_decode(bytes, prefix, list_size_format)
        for _ in range(list_size):
            (item_size, ), prefix = cut_and_decode(bytes, prefix, item_size_format)
            config.append(bytes[prefix: prefix + item_size].decode())
            prefix += item_size
        return Config(config)


class Snapshot:
    config = [
        'timestamp',
        'translation',
        'rotation',
        'color_image',
        'depth_image',
        'feelings',
    ]

    def __init__(self, timestamp: datetime, translation, rotation, color_image: Image.Image, depth_image: Image.Image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def set_default(self, key):
        if key == 'timestamp':
            self.timestamp =  datetime.fromtimestamp(0)
        elif key == 'translation':
            self.translation = (0, 0, 0)
        elif key == 'rotation':
            self.rotation = (0, 0, 0, 0)
        elif key == 'color_image':
            self.color_image = Image.new('RGB', (0, 0))
        elif key == 'depth_image':
            self.depth_image = Image.new('F', (0, 0))
        elif key == 'feelings':
            self.feelings = (0, 0, 0, 0)

        
    def serialize(self):
        return struct.pack(timestamp_format, int(self.timestamp.timestamp() * 1000)) \
            + struct.pack(translation_format, *self.translation) \
            + struct.pack(rotation_format, *self.rotation) \
            + struct.pack(width_format, self.color_image.width) \
            + struct.pack(height_format, self.color_image.height) \
            + self.color_image.tobytes() \
            + struct.pack(width_format, self.depth_image.width) \
            + struct.pack(height_format, self.depth_image.height) \
            + self.depth_image.tobytes() \
            + struct.pack(feelings_format, *self.feelings)

    @classmethod
    def from_bytes(cls, bytes: bytes):
        prefix = 0
        (timestamp, ), prefix = cut_and_decode(bytes, prefix, timestamp_format)
        timestamp = datetime.fromtimestamp(timestamp / 1000)
        translation, prefix = cut_and_decode(bytes, prefix, translation_format)
        rotation, prefix = cut_and_decode(bytes, prefix, rotation_format)
        color_image, prefix = image_cut_and_decode(bytes, prefix, 'RGB')
        depth_image, prefix = image_cut_and_decode(bytes, prefix, 'F')
        feelings, prefix = cut_and_decode(bytes, prefix, feelings_format)
        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)


def cut_and_decode(bytes: bytes, prefix: int, format: str) -> tuple[tuple, int]:
    size = struct.calcsize(format)
    suffix = prefix + size
    return struct.unpack(format, bytes[prefix: suffix]), suffix


def image_cut_and_decode(bytes: bytes, prefix: int, mode: str) -> tuple[Image.Image, int]:
    (width, ), prefix = cut_and_decode(bytes, prefix, width_format)
    (height, ), prefix = cut_and_decode(bytes, prefix, height_format)
    if not height or not width:
        return Image.new(mode, (width, height)), prefix
    if mode == 'RGB':
        suffix = prefix + height * width * 3
        image_data = bytes[prefix: suffix]
    elif mode == 'F':
        suffix = prefix + height * width * struct.calcsize(pixel_format)
        image_data = bytes[prefix: suffix]
    else:
        raise ValueError(f'Mode {mode} no supported :[')
    return Image.frombytes(mode, (width, height), image_data, 'raw'), suffix
