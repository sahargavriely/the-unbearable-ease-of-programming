class TypedProperty:
    def __init__(self, type):
        self.name = None
        self.type = type

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self.type()
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise ValueError(f'Attribute {self.name!r} must be {self.type}')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        instance.__dict__[self.name] = self.type()
