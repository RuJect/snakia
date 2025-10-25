import gc
import sys
from types import FunctionType, MethodType
from typing import Any


def this() -> Any:
    """Get the current function."""
    frame = sys._getframe(1)
    for obj in gc.get_objects():
        if isinstance(obj, FunctionType):
            if obj.__code__ is frame.f_code:
                return obj
        elif isinstance(obj, MethodType):
            if obj.__func__.__code__ is frame.f_code:
                return obj
    return None
