from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from .event import Event

type Filter[T: Event] = Callable[[T], bool]


class BaseFilter[T: Event](ABC):
    @abstractmethod
    def __call__(self, event: T) -> bool: ...
