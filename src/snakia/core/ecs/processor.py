from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from .system import System


class Processor(ABC):
    """
    A processor is a class that processes the system.
    """

    before: ClassVar[tuple[type[Processor], ...]] = ()
    after: ClassVar[tuple[type[Processor], ...]] = ()

    @abstractmethod
    def process(self, system: System) -> None:
        """
        Processes the system. Called once per update.

        Args:
            system (System): The system to process.
        """
