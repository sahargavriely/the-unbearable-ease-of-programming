import datetime as dt
import struct


class Thought:
    _str_format = '%F %T'
    _file_format = '%F_%H-%M-%S'
    header_format = '<QQI'
    header_size = struct.calcsize(header_format)

    def __init__(self, user_id: int, timestamp: dt.datetime, thought: str):
        self.thought = thought
        self.timestamp = timestamp
        self.user_id = user_id

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        thought = self.thought
        timestamp = self.timestamp
        user_id = self.user_id
        return f'{cls_name}({user_id=!r}, {timestamp=!r}, {thought=!r})'

    def __str__(self) -> str:
        thought = self.thought
        user_id = self.user_id
        return f'[{self.str_formatted_timestamp}] user {user_id}: {thought}'

    def __eq__(self, other) -> bool:
        return isinstance(other, Thought) \
            and self.timestamp == other.timestamp \
            and self.thought == other.thought \
            and self.user_id == other.user_id

    @property
    def file_formatted_timestamp(self) -> str:
        return self.timestamp.strftime(self._file_format)

    @property
    def str_formatted_timestamp(self) -> str:
        return self.timestamp.strftime(self._str_format)

    def serialize(self) -> bytes:
        timestamp = int(self.timestamp.timestamp())
        thought = self.thought.encode()
        user_id = self.user_id
        size = len(thought)
        headers = struct.pack(self.header_format, user_id, timestamp, size)
        return headers + thought

    @classmethod
    def deserialize(cls, data: bytes):
        headers = data[:cls.header_size]
        user_id, timestamp, _ = struct.unpack(cls.header_format, headers)
        timestamp = dt.datetime.fromtimestamp(timestamp)
        thought = data[cls.header_size:].decode()
        return Thought(user_id, timestamp, thought)
