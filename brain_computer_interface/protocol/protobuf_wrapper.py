import importlib
import inspect
import numbers

from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType


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

    def jsonify(self) -> dict:
        json_obj = dict()
        for attr in dir(self):
            if attr.startswith('_') \
               or inspect.ismethod(getattr(self, attr)):
                continue
            val = getattr(self, attr)
            if isinstance(val, ProtobufWrapper):
                json_obj[attr] = val.jsonify()
            elif isinstance(val, (list, bytes, str, numbers.Number)):
                # assuming lists are already in json format
                json_obj[attr] = val
        return json_obj

    def to_protobuf(self):
        protobuf_obj = self._protobuf_type()
        for attr in dir(self):
            if attr.startswith('_') \
               or inspect.ismethod(getattr(self, attr)):
                continue
            val = getattr(self, attr)
            if isinstance(val, ProtobufWrapper):
                getattr(protobuf_obj, attr).CopyFrom(val.to_protobuf())
            elif isinstance(val, (bytes, str, numbers.Number)):
                setattr(protobuf_obj, attr, val)
            elif isinstance(val, list):
                getattr(protobuf_obj, attr).extend(val)
        return protobuf_obj

    def serialize(self) -> bytes:
        protobuf_obj = self.to_protobuf()
        return protobuf_obj.SerializeToString()

    @classmethod
    def from_json(cls, json_obj: dict):
        obj = cls()
        for attr in dir(obj):
            if any((attr.startswith('_'),
                    inspect.ismethod(getattr(obj, attr)),
                    attr not in json_obj)):
                continue
            val = json_obj[attr]
            if isinstance(val, dict):
                setattr(obj, attr,
                        _get_protobuf_wrapped_class(attr).from_json(val))
            elif isinstance(val, (list, bytes, str, numbers.Number)):
                setattr(obj, attr, val)
        return obj

    @classmethod
    def from_protobuf(cls, protobuf_obj):
        obj = cls()
        for attr in dir(obj):
            if any((attr.startswith('_'),
                    inspect.ismethod(getattr(obj, attr)),
                    not hasattr(protobuf_obj, attr))):
                continue
            val = getattr(protobuf_obj, attr)
            if isinstance(type(val), GeneratedProtocolMessageType):
                setattr(obj, attr,
                        _get_protobuf_wrapped_class(attr).from_protobuf(val))
            elif isinstance(val, (list, bytes, str, numbers.Number)):
                setattr(obj, attr, val)
            else:  # isinstance(val, RepeatedScalarContainer):
                setattr(obj, attr, list(val))
        return obj

    @classmethod
    def from_bytes(cls, bytes: bytes):
        protobuf_obj = cls._protobuf_type()
        protobuf_obj.ParseFromString(bytes)
        return cls.from_protobuf(protobuf_obj)


def _get_protobuf_wrapped_class(cls_name: str) -> ProtobufWrapper:
    cls_name = ''.join(word.capitalize() for word in cls_name.split('_'))
    if not classes:
        protocol = importlib.import_module('.protocol', __package__)
        for name, obj in inspect.getmembers(protocol, inspect.isclass):
            classes[name] = obj
    return classes[cls_name]
