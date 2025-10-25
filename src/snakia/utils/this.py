import gc
from types import FunctionType, MethodType
from typing import Any

from .frame import frame


def this() -> Any:
    """Get the current function."""
    f = frame()
    for obj in gc.get_objects():
        if isinstance(obj, FunctionType):
            if obj.__code__ is f.f_code:
                return obj
        elif isinstance(obj, MethodType):
            if obj.__func__.__code__ is f.f_code:
                return obj
    return None
