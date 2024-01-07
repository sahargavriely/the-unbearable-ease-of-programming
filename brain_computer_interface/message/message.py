from datetime import datetime as dt
from enum import Enum
import gzip
import struct

from . import mind_pb2
from .protobuf_wrapper import ProtobufWrapper
from ..utils import keys


TYPE_FORMAT = '<I'
TYPE_FORMAT_SIZE = struct.calcsize(TYPE_FORMAT)

CONFIG_OPTIONS = [
    # keys.datetime,
    keys.pose,
    keys.color_image,
    keys.depth_image,
    keys.feelings,
]


class Types(Enum):
    MIND = 0
    THOUGHT = 1


class User(ProtobufWrapper):
    _protobuf_type = mind_pb2.User

    def __init__(self, id: int, name: str, birthday: int, gender: int):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.gender = gender

    def __repr__(self) -> str:
        gender = 'male' if not self.gender \
            else 'female' if self.gender == 1 \
            else 'unicorn'
        return f'<{self.__class__.__name__} {self.id}: {self.name}, ' \
            f'born {dt.fromtimestamp(self.birthday):%B %d, %Y} ({gender})>'


class Config(ProtobufWrapper):
    _protobuf_type = mind_pb2.Config

    def __init__(self, config: list[str]):
        self.config = config

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.config}>'

    def __contains__(self, key):
        return key in self.config


class Translation(ProtobufWrapper):
    _protobuf_type = mind_pb2.Pose.Translation  # type: ignore

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'


class Rotation(ProtobufWrapper):
    _protobuf_type = mind_pb2.Pose.Rotation  # type: ignore

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z}, {self.w})'


class Pose(ProtobufWrapper):
    _protobuf_type = mind_pb2.Pose

    def __init__(self, translation: Translation, rotation: Rotation):
        self.translation = translation
        self.rotation = rotation

    def __repr__(self) -> str:
        return f'{self.translation} / {self.rotation}'


class ColorImage(ProtobufWrapper):
    _protobuf_type = mind_pb2.ColorImage

    def __init__(self, width: int, height: int, data: bytes):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.width}X{self.height}>'

    def jsonify(self, path=None) -> dict:
        if path is None:
            return super().jsonify(path)
        save_as = f'{path}/{keys.color_image}'
        with gzip.open(save_as, 'wb') as f:
            f.write(self.data)  # type: ignore
        self.data = save_as
        return super().jsonify(path)

    @classmethod
    def from_json(cls, json_obj: dict):
        if not isinstance(json_obj[keys.data], str):
            return super().from_json(json_obj)
        json_obj = json_obj.copy()
        with gzip.open(json_obj[keys.data], 'rb') as file:
            json_obj[keys.data] = file.read()
        return super().from_json(json_obj)


class DepthImage(ProtobufWrapper):
    _protobuf_type = mind_pb2.DepthImage

    def __init__(self, width: int, height: int, data: list[float]):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.width}X{self.height}>'

    def jsonify(self, path=None) -> dict:
        if path is None:
            return super().jsonify(path)
        save_as = f'{path}/{keys.depth_image}'
        with gzip.open(save_as, 'wb') as f:
            f.write(struct.pack(f'{len(self.data)}f', *self.data))
        self.data = save_as
        return super().jsonify(path)

    @classmethod
    def from_json(cls, json_obj: dict):
        if not isinstance(json_obj[keys.data], str):
            return super().from_json(json_obj)
        json_obj = json_obj.copy()
        with gzip.open(json_obj[keys.data], 'rb') as file:
            json_obj[keys.data] = list(struct.unpack(
                f'{json_obj[keys.height] * json_obj[keys.width]}f',
                file.read()))  # type: ignore
        return super().from_json(json_obj)


class Feelings(ProtobufWrapper):
    _protobuf_type = mind_pb2.Feelings

    def __init__(self, hunger: float, thirst: float, exhaustion: float,
                 happiness: float):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
            f'{self.hunger:.3f}, {self.thirst:.3f}, ' \
            f'{self.exhaustion:.3f}, {self.happiness:.3f}>'


class Snapshot(ProtobufWrapper):
    _protobuf_type = mind_pb2.Snapshot

    def __init__(
        self,
        datetime: int,
        pose: Pose,
        color_image: ColorImage,
        depth_image: DepthImage,
        feelings: Feelings
    ):
        self.datetime = datetime
        self.pose = pose
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self) -> str:
        datetime = dt.fromtimestamp(self.datetime / 1000)
        return f'<{self.__class__.__name__} at ' \
            f'{datetime:%B %d, %Y at %T.%f} on {self.pose} ' \
            f'with a {self.color_image}, a {self.depth_image} ' \
            f'and {self.feelings}>'

    def set_default(self, key):
        if key == keys.datetime:
            self.datetime = 0
        elif key == keys.pose:
            self.pose.translation = Translation(0, 0, 0)
            self.pose.rotation = Rotation(0, 0, 0, 0)
        elif key == keys.color_image:
            self.color_image = ColorImage(0, 0, b'')
        elif key == keys.depth_image:
            self.depth_image = DepthImage(0, 0, list())
        elif key == keys.feelings:
            self.feelings = Feelings(0, 0, 0, 0)
