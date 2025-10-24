import sys
from types import FrameType


def frame() -> FrameType:
    return sys._getframe(1)
