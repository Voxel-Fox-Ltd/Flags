from __future__ import annotations

import functools
from typing import Any, Type, Optional


__all__ = (
    'Flags',
    'flag_value',
)


class flag_value:

    __slots__ = (
        'name',
        'value',
        '_func',
        '__doc__',
    )

    def __init__(self, func, name: Optional[str] = None):
        self.name = func.__name__ or name
        self.value = func(None)
        self._func = func

    def __get__(self, instance: Flags, cls: Type[Flags]) -> bool:
        return bool(instance.value & self.value)

    def __set__(self, instance: Flags, new_value: bool):
        if new_value:
            instance.value |= self.value
        else:
            instance.value &= ~self.value

    def __call__(self, instance: Any):
        return self.value


class Flags:

    def __new__(cls, *args, **kwargs):
        # See if we want to build from cls.CREATE_FLAGS
        if (current_flags := getattr(cls, "CREATE_FLAGS", None)):
            if not isinstance(current_flags, dict):
                raise TypeError("Existing CREATE_FLAGS attribute should be dict")
            for name, value in current_flags.items():
                doc = None
                if isinstance(value, tuple):
                    value, doc = value
                def wrapper(_):
                    return value
                wrapper.__doc__ = doc
                setattr(cls, name, flag_value(wrapper, name))

        # Build flag values
        cls.VALID_FLAGS = {}
        for i, o in cls.__dict__.items():
            if not isinstance(o, flag_value):
                continue
            cls.VALID_FLAGS[i] = o(None)
            o.__doc__ = o._func.__doc__
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
