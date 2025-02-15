from builtins import TypeError
from typing import Callable, Dict


class Event:
    _callbacks: list[callable]

    def __init__(self):
        self._callbacks = []

    def __get__(self, obj, objtype=None):
        return self

    def __set__(self, obj, value):
        if isinstance(value, Event):
            self._callbacks = value._callbacks
        elif isinstance(value, list):
            if all(isinstance(v, Callable) for v in value):
                self._callbacks = value
        elif isinstance(value, Callable):
            self._callbacks = [value]

    def __add__(self, clb):
        if isinstance(clb, Callable):
            self._callbacks.append(clb)
        elif isinstance(clb, list):
            for c in clb:
                if isinstance(c, Callable):
                    self._callbacks.append(c)
        return self

    def __call__(self):
        [clb() for clb in self._callbacks if isinstance(clb, Callable)]
