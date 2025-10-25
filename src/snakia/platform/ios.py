from __future__ import annotations

from typing import Literal

from .layer import PlatformLayer
from .os import PlatformOS


# TODO: create a ios layer
class IosLayer(PlatformLayer[Literal[PlatformOS.IOS]]):
    target = PlatformOS.IOS
