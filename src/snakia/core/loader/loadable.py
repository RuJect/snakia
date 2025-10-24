from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from snakia.core.engine import Engine


class Loadable(ABC):
    @abstractmethod
    def __init__(self, engine: Engine) -> None: ...

    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def unload(self) -> None: ...
