from __future__ import annotations

from typing import Literal

from .layer import PlatformLayer
from .os import PlatformOS


# TODO: create a windows layer
class WindowsLayer(PlatformLayer[Literal[PlatformOS.WINDOWS]]):
    target = PlatformOS.WINDOWS
