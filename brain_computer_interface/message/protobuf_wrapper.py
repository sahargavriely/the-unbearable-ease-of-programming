from collections.abc import Iterable
import importlib
import inspect
import numbers
import re

from . import mind_pb2


classes = dict()


def _raise_attribute_error():
    raise AttributeError('Missing _protobuf_type attribute')


class ProtobufWrapper:
    _protobuf_type = _raise_attribute_error

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, self.__class__) \
            and all(getattr(self, attr) == getattr(__value, attr)
                    for attr in dir(self)
                    if not attr.startswith('_')
                    and not inspect.ismethod(getattr(self, attr)))

    def jsonify(self, path=None) -> dict:
        json_obj = dict()
        for attr in dir(self):
            if attr.startswith('_'):
                continue
            val = getattr(self, attr)
            if isinstance(val, ProtobufWrapper):
                json_obj[attr] = val.jsonify(path)
            elif isinstance(val, (bytes, str, numbers.Number)):
                json_obj[attr] = val
            elif isinstance(val, Iterable):
                json_obj[attr] = list(val)
        return json_obj

    def to_protobuf(self):
        protobuf_obj = self._protobuf_type()
        for attr in dir(self):
            if attr.startswith('_'):
                continue
            val = getattr(self, attr)
            if isinstance(val, ProtobufWrapper):
                getattr(protobuf_obj, attr).CopyFrom(val.to_protobuf())
            elif isinstance(val, (bytes, str, numbers.Number)):
                setattr(protobuf_obj, attr, val)
            elif isinstance(val, (list, Iterable)):
                getattr(protobuf_obj, attr).extend(val)
        return protobuf_obj

    def serialize(self) -> bytes:
        protobuf_obj = self.to_protobuf()
        return protobuf_obj.SerializeToString()

    @classmethod
    def from_json(cls, json_obj: dict):
        args = list()
        for arg_name in inspect.getfullargspec(cls).args[1:]:
            arg = json_obj[arg_name]
            if isinstance(arg, dict):
                arg = _get_protobuf_wrapped_class(arg_name).from_json(arg)
            args.append(arg)
        return cls(*args)

    @classmethod
    def from_protobuf(cls, protobuf_obj):
        args = list()
        for arg_name in inspect.getfullargspec(cls).args[1:]:
            arg = getattr(protobuf_obj, arg_name)
            pattern = mind_pb2.__name__ + r'\.([\w\.]+)'
            match = re.search(pattern, str(type(arg)))
            if match:
                arg = _get_protobuf_wrapped_class(arg_name).from_protobuf(arg)
            args.append(arg)
        return cls(*args)

    @classmethod
    def from_bytes(cls, bytes: bytes):
        protobuf_obj = cls._protobuf_type()
        protobuf_obj.ParseFromString(bytes)
        return cls.from_protobuf(protobuf_obj)


def _get_protobuf_wrapped_class(cls_name: str) -> ProtobufWrapper:
    cls_name = ''.join(word.capitalize() for word in cls_name.split('_'))
    if not classes:
        message = importlib.import_module('.message', __package__)
        for name, obj in inspect.getmembers(message, inspect.isclass):
            classes[name] = obj
    return classes[cls_name]
