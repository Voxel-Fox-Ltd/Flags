from __future__ import annotations
from collections.abc import Callable, Generator, Iterable

import functools
from typing import Any, ClassVar, Type, Optional
from typing_extensions import Self

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

    name: str
    value: int

    def __init__(self, func: Callable[[Any], int], name: Optional[str] = None):
        self.name: str = name or func.__name__
        self.value: int = func(None)
        self._func: Callable[[Any], int] = func

    def __repr__(self) -> str:
        return f"<flag_value name={self.name} value={self.value}>"

    def __get__(self, instance: Flags, cls: Type[Flags]) -> bool:
        return bool(instance.value & self.value)

    def __set__(self, instance: Flags, new_value: bool):
        if new_value:
            instance.value |= self.value
        else:
            instance.value &= ~self.value

    def __call__(self, instance: Any):
        return self.value


class FlagMeta(type):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        # See if we want to build from cls.CREATE_FLAGS
        if (current_flags := getattr(cls, "CREATE_FLAGS", None)):
            if not isinstance(current_flags, dict):
                raise TypeError("Existing CREATE_FLAGS attribute should be dict")
            for nname, value in current_flags.items():
                doc = None
                if isinstance(value, tuple):
                    value, doc = value
                def wrapper(_):
                    return value
                wrapper.__doc__ = doc
                setattr(cls, nname, flag_value(wrapper, nname))

        # Build flag values
        docbuilder = cls.__doc__ or ""
        attribute_lines: list[str] = []
        aliases = getattr(cls, "ALIASES", [])
        cls.VALID_FLAGS = {}
        for i, o in cls.__dict__.items():
            if not isinstance(o, flag_value):
                continue
            cls.VALID_FLAGS[i] = o(None)
            cls.__annotations__[i] = bool
            o.__doc__ = o._func.__doc__
            if i not in aliases:
                attribute_lines.append(f"{i} : bool")
                if o.__doc__:
                    attribute_lines.append(f"\t{o.__doc__}")

        # See if we wanna build some docstrings
        if "Attributes" not in [line.strip() for line in docbuilder.split("\n")]:
            cls.__doc__ = (
                docbuilder.strip()
                + "\n\nAttributes\n----------\n"
                + "\n".join(attribute_lines)
            )


class Flags(metaclass=FlagMeta):

    value: int
    CREATE_FLAGS: ClassVar[dict[str, int]]
    VALID_FLAGS: ClassVar[dict[str, int]]
    ALIASES: ClassVar[Iterable[str]] = ()

    def __init__(self, value: int = 0, **kwargs: bool):
        self.value = value
        for i, o in kwargs.items():
            setattr(self, i, o)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(0b{self.value:_b})"

    def walk(self) -> Generator[tuple[str, bool], None, None]:
        """
        Walk through the names and values of the flags.
        """

        for name in self.VALID_FLAGS:
            val: bool = getattr(self, name)
            if name in self.ALIASES:
                continue
            yield name, val

    def update(self, **kwargs: bool) -> Self:
        """
        Set flag values in-place for the given instance.
        """

        for i, o in kwargs.items():
            setattr(self, i, o)

    @classmethod
    def all(cls) -> Self:
        """
        Get an instance of this class with all attributes set to ``True``.
        """

        v = functools.reduce(lambda a, b: a | b, cls.VALID_FLAGS.values())
        return cls(v)

    @classmethod
    def none(cls) -> Self:
        """
        Get an instance of this class with all attributes set to ``False``.
        """

        return cls(0)

    def __eq__(self, other) -> bool:
        # Make sure they're flags
        if not isinstance(other, Flags):
            raise ValueError("Cannot compare incompatible types")

        # Easy compare - same type
        if isinstance(other, self.__class__):
            return self.value == other.value

        # Harder compare - a different type but may have compatible attributes
        return (
            self.value == other.value
            and self.VALID_FLAGS == other.VALID_FLAGS
        )
