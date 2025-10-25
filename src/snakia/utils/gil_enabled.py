from typing import TYPE_CHECKING, Final


if TYPE_CHECKING:
    GIL_ENABLED: Final[bool] = bool(...)
    """
    Whether the GIL is enabled."""
else:
    import sys

    if sys.version_info >= (3, 13):
        GIL_ENABLED = sys._is_gil_enabled()
    else:
        GIL_ENABLED = True
