from __future__ import annotations

from typing import Literal

from .layer import PlatformLayer
from .os import PlatformOS


# TODO: create a freebds layer
class FreebsdLayer(PlatformLayer[Literal[PlatformOS.FREEBSD]]):
    target = PlatformOS.FREEBSD
