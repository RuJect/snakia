from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Final, cast, final

from snakia.core.ecs import System
from snakia.core.es import Dispatcher
from snakia.core.loader import Loadable

if TYPE_CHECKING:
    from snakia.core.engine import Engine
    from snakia.core.loader import Meta


class Plugin(Loadable):
    meta: Final[Meta] = cast("Meta", ...)

    @final
    def __init__(self, engine: Engine) -> None:
        self.__engine: Final = engine

    @final
    @property
    def dispatcher(self) -> Dispatcher:
        return self.__engine.dispatcher

    @final
    @property
    def system(self) -> System:
        return self.__engine.system

    @final
    def load(self) -> None:
        for processor in self.meta.processors:
            self.__engine.system.add_processor(processor(self))
        for event_type, subscriber in self.meta.subscribers:
            self.__engine.dispatcher.subscribe(event_type, subscriber)
        self.on_load()

    @final
    def unload(self) -> None:
        for processor in self.meta.processors:
            self.__engine.system.remove_processor(processor)
        for event_type, subscriber in self.meta.subscribers:
            self.__engine.dispatcher.unsubscribe(event_type, subscriber)
        self.on_unload()

    @abstractmethod
    def on_load(self) -> None:
        pass

    @abstractmethod
    def on_unload(self) -> None:
        pass

    if TYPE_CHECKING:

        @final
        def __init_subclass__(cls, meta: Meta) -> None:
            pass

    else:

        def __init_subclass__(cls, meta: Meta) -> None:
            cls.meta = meta
