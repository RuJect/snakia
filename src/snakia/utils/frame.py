import sys
from types import FrameType


def frame() -> FrameType:
    """Get the current frame."""
    return sys._getframe(1)
