from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Final

if TYPE_CHECKING:
    from snakia.core.engine import Engine
    from snakia.core.loader import Loadable


class Loader:
    def __init__(self, engine: Engine) -> None:
        self.__engine: Final = engine
        self.__loadables: Final[list[Loadable]] = []

    def register(self, loadable: Callable[[Engine], Loadable]) -> None:
        self.__loadables.append(loadable(self.__engine))

    def load_all(self) -> None:
        for loadable in self.__loadables:
            loadable.load()

    def unload_all(self) -> None:
        for loadable in reversed(self.__loadables):
            loadable.unload()
