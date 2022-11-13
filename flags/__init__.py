from __future__ import annotations

import functools
from typing import Dict, Type


__all__ = (
    'Flags',
    'flag_value',
)


class flag_value:

    def __init__(self, func):
        self.name = func.__name__
        self.value = func(None)       

    def __get__(self, instance: Flags, cls: Type[Flags]) -> bool:
        return bool(instance.value & self.value)

    def __set__(self, instance: Flags, new_value: bool):
        if new_value:
            instance.value |= self.value
        else:
            instance.value &= ~self.value

    def __call__(self, instance: Flags):
        return self.value


class Flags:

    def __new__(cls, *args, **kwargs):
        cls.VALID_FLAGS = {}
        for i, o in cls.__dict__.items():
            if isinstance(o, flag_value):
                cls.VALID_FLAGS[i] = o(None)
        return super().__new__(cls)

    def __init__(self, value: int = 0, **kwargs):
        self.value = value
        for i, o in kwargs.items():
            setattr(self, i, o)

    def __repr__(self) -> str:
        d = []
        for i in self.VALID_FLAGS.keys():
            d.append(f"{i}={getattr(self, i)}")
        return f"{self.__class__.__name__}({', '.join(d)})"

    @classmethod
    def all(cls):
        v = functools.reduce(lambda a, b: a | b, cls.VALID_FLAGS.values())
        return cls(v)

    @classmethod
    def none(cls):
        return cls(0)
