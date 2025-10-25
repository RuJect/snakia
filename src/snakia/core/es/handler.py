from __future__ import annotations

from typing import Optional, Protocol

from .action import Action
from .event import Event


class Handler[T: Event](Protocol):
    """Handler for an event."""

    def __call__(self, event: T) -> Optional[Action]: ...
