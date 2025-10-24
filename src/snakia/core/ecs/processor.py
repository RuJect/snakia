from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from .system import System


class Processor(ABC):
    before: ClassVar[tuple[type[Processor], ...]] = ()
    after: ClassVar[tuple[type[Processor], ...]] = ()

    @abstractmethod
    def process(self, system: System) -> None: ...
