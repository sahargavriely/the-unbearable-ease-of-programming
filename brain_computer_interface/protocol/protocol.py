from datetime import datetime as dt
from enum import Enum
import struct

from . import mind_pb2


TYPE_FORMAT = '<I'
TYPE_FORMAT_SIZE = struct.calcsize(TYPE_FORMAT)


class Types(Enum):
    MIND = 0
    THOUGHT = 1


class Gender(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2


class User:
    def __init__(self, id: int, name: str, birthday: int, gender: int):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.gender = gender

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.id}: {self.name}, ' \
            f'born {dt.fromtimestamp(self.birthday):%B %d, %Y} ' \
            f'({Gender(self.gender)})>'

    def serialize(self) -> bytes:
        user = mind_pb2.User()
        user.id = self.id
        user.name = self.name
        user.birthday = self.birthday
        user.gender = self.gender
        return user.SerializeToString()

    @classmethod
    def from_bytes(cls, bytes: bytes):
        user = mind_pb2.User()
        user.ParseFromString(bytes)
        return User(user.id, user.name, user.birthday, user.gender)


class Config:
    def __init__(self, config: list[str]):
        self.config = config

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.config}>'

    def __contains__(self, key):
        return key in self.config

    def serialize(self):
        config = mind_pb2.Config()
        config.config.extend(self.config)
        return config.SerializeToString()

    @classmethod
    def from_bytes(cls, bytes: bytes):
        config = mind_pb2.Config()
        config.ParseFromString(bytes)
        return Config(config.config)


class Translation:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'


class Rotation:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z}, {self.w})'


class Pose:
    def __init__(self, translation: Translation, rotation: Rotation):
        self.translation = translation
        self.rotation = rotation

    def __repr__(self) -> str:
        return f'{self.translation} / {self.rotation}'


class ColorImage:
    def __init__(self, width: int, height: int, data: bytes):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
            f'{self.width}X{self.height}>'


class DepthImage:
    def __init__(self, width: int, height: int, data: list[float]):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
            f'{self.width}X{self.height}>'


class Feelings:
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


class Snapshot:
    config = [
        'datetime',
        'translation',
        'rotation',
        'color_image',
        'depth_image',
        'feelings',
    ]

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
        if key == 'datetime':
            self.datetime = 0
        elif key == 'translation':
            self.pose.translation = Translation(0, 0, 0)
        elif key == 'rotation':
            self.pose.rotation = Rotation(0, 0, 0, 0)
        elif key == 'color_image':
            self.color_image = ColorImage(0, 0, b'')
        elif key == 'depth_image':
            self.depth_image = DepthImage(0, 0, list())
        elif key == 'feelings':
            self.feelings = Feelings(0, 0, 0, 0)

    def serialize(self) -> bytes:
        snapshot = mind_pb2.Snapshot()
        snapshot.datetime = self.datetime
        pose = mind_pb2.Pose()
        translation = pose.translation
        translation.x = self.pose.translation.x
        translation.y = self.pose.translation.y
        translation.z = self.pose.translation.z
        rotation = pose.rotation
        rotation.x = self.pose.rotation.x
        rotation.y = self.pose.rotation.y
        rotation.z = self.pose.rotation.z
        rotation.w = self.pose.rotation.w
        snapshot.pose.CopyFrom(pose)
        color_image = mind_pb2.ColorImage()
        color_image.width = self.color_image.width
        color_image.height = self.color_image.height
        color_image.data = self.color_image.data
        snapshot.color_image.CopyFrom(color_image)
        depth_image = mind_pb2.DepthImage()
        depth_image.width = self.depth_image.width
        depth_image.height = self.depth_image.height
        depth_image.data.extend(self.depth_image.data)
        snapshot.depth_image.CopyFrom(depth_image)
        feelings = mind_pb2.Feelings()
        feelings.hunger = self.feelings.hunger
        feelings.thirst = self.feelings.thirst
        feelings.exhaustion = self.feelings.exhaustion
        feelings.happiness = self.feelings.happiness
        snapshot.feelings.CopyFrom(feelings)
        return snapshot.SerializeToString()

    @classmethod
    def from_bytes(cls, bytes: bytes):
        snapshot = mind_pb2.Snapshot()
        snapshot.ParseFromString(bytes)
        translation = snapshot.pose.translation
        translation = Translation(translation.x, translation.y, translation.z)
        rotation = snapshot.pose.rotation
        rotation = Rotation(rotation.x, rotation.y, rotation.z, rotation.w)
        feelings = snapshot.feelings
        feelings = Feelings(feelings.hunger, feelings.thirst,
                            feelings.exhaustion, feelings.happiness)
        color_im = snapshot.color_image
        depth_im = snapshot.depth_image
        return Snapshot(
            snapshot.datetime,
            Pose(translation, rotation),
            ColorImage(color_im.width, color_im.height, color_im.data),
            DepthImage(depth_im.width, depth_im.height, depth_im.data),
            feelings
        )
