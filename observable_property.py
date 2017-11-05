from enum import Enum
from typing import TypeVar, List, Generic, Callable, Iterable, NamedTuple

T = TypeVar('T')


class Prop(Generic[T]):

    def __init__(self, value: T, callbacks: Iterable[Callable[[T], None]] = None)->None:
        self._value = value
        self.callbacks: List[Callable[[T], None]] = [x for x in callbacks] if callbacks else []

    def connect(self, callback: Callable[[T], None])->None:
        callback(self._value)
        self.callbacks.append(callback)

    @property
    def value(self)->T:
        return self._value

    @value.setter
    def value(self, value: T):
        if self._value == value:
            return
        self._value = value
        self.emit(self._value)

    def emit(self, value: T):
        # logger.debug('emit')
        for x in self.callbacks:
            x(value)


class ListPropEvent(Enum):
    Updated = 0
    Added = 1
    Removed = 2
    Cleared = 3


class ListProp(Generic[T]):
    def __init__(self, values: List[T])->None:
        self.values: List[T] = values[:]
        self.callbacks: List[Callable[[ListPropEvent, Iterable[T]], None]] = []

    def connect(self, callback: Callable[[ListPropEvent, Iterable[T]], None])->None:
        callback(ListPropEvent.Updated, self.values)
        self.callbacks.append(callback)


class RGBAf(NamedTuple):
    red: float = 1.0
    green: float = 1.0
    blue: float = 1.0
    alpha: float = 1.0
