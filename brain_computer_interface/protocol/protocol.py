from datetime import datetime as dt
from enum import Enum
import struct

from . import mind_pb2
from .protobuf_wrapper import ProtobufWrapper
from ..utils import TypedProperty


TYPE_FORMAT = '<I'
TYPE_FORMAT_SIZE = struct.calcsize(TYPE_FORMAT)

CONFIG_OPTIONS = [
    'datetime',
    'pose',
    # 'translation',
    # 'rotation',
    'color_image',
    'depth_image',
    'feelings',
]


class Types(Enum):
    MIND = 0
    THOUGHT = 1


class User(ProtobufWrapper):
    _protobuf_type = mind_pb2.User

    id = TypedProperty(int)
    name = TypedProperty(str)
    birthday = TypedProperty(int)
    gender = TypedProperty(int)

    def __repr__(self) -> str:
        gender = 'male' if not self.gender \
            else 'female' if self.gender == 1 \
            else 'unicorn'
        return f'<{self.__class__.__name__} {self.id}: {self.name}, ' \
            f'born {dt.fromtimestamp(self.birthday):%B %d, %Y} ({gender})>'


class Config(ProtobufWrapper):
    _protobuf_type = mind_pb2.Config

    config = TypedProperty(list)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.config}>'

    def __contains__(self, key):
        return key in self.config


class Translation(ProtobufWrapper):
    _protobuf_type = mind_pb2.Pose.Translation  # type: ignore

    x = TypedProperty(float)
    y = TypedProperty(float)
    z = TypedProperty(float)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'


class Rotation(ProtobufWrapper):
    _protobuf_type = mind_pb2.Pose.Rotation  # type: ignore

    x = TypedProperty(float)
    y = TypedProperty(float)
    z = TypedProperty(float)
    w = TypedProperty(float)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z}, {self.w})'


class Pose(ProtobufWrapper):
    _protobuf_type = mind_pb2.Pose

    translation = TypedProperty(Translation)
    rotation = TypedProperty(Rotation)

    def __repr__(self) -> str:
        return f'{self.translation} / {self.rotation}'


class ColorImage(ProtobufWrapper):
    _protobuf_type = mind_pb2.ColorImage

    width = TypedProperty(int)
    height = TypedProperty(int)
    data = TypedProperty(bytes)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.width}X{self.height}>'


class DepthImage(ProtobufWrapper):
    _protobuf_type = mind_pb2.DepthImage

    width = TypedProperty(int)
    height = TypedProperty(int)
    data = TypedProperty(list)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.width}X{self.height}>'


class Feelings(ProtobufWrapper):
    _protobuf_type = mind_pb2.Feelings

    hunger = TypedProperty(float)
    thirst = TypedProperty(float)
    exhaustion = TypedProperty(float)
    happiness = TypedProperty(float)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
            f'{self.hunger:.3f}, {self.thirst:.3f}, ' \
            f'{self.exhaustion:.3f}, {self.happiness:.3f}>'


class Snapshot(ProtobufWrapper):
    _protobuf_type = mind_pb2.Snapshot

    datetime = TypedProperty(int)
    pose = TypedProperty(Pose)
    color_image = TypedProperty(ColorImage)
    depth_image = TypedProperty(DepthImage)
    feelings = TypedProperty(Feelings)

    def __repr__(self) -> str:
        datetime = dt.fromtimestamp(self.datetime / 1000)
        return f'<{self.__class__.__name__} at ' \
            f'{datetime:%B %d, %Y at %T.%f} on {self.pose} ' \
            f'with a {self.color_image}, a {self.depth_image} ' \
            f'and {self.feelings}>'
