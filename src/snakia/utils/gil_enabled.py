import sys

if sys.version_info >= (3, 13):
    GIL_ENABLED = sys._is_gil_enabled()
else:
    GIL_ENABLED: bool = True

__all__ = ["GIL_ENABLED"]
