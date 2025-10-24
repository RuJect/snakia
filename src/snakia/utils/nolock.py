from typing import TYPE_CHECKING

from .gil_enabled import GIL_ENABLED

if TYPE_CHECKING:

    def nolock() -> None: ...

else:

    if GIL_ENABLED:
        import time

        def nolock() -> None:
            time.sleep(0.001)

    else:

        def nolock() -> None:
            pass
