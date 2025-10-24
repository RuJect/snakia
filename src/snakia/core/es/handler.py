from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional

from .action import Action
from .event import Event

type Handler[T: Event] = Callable[[T], Optional[Action]]


class BaseHandler[T: Event](ABC):
    @abstractmethod
    def __call__(self, event: T) -> Optional[Action]: ...
