import threading
from typing import Final

from snakia.core.ecs import System
from snakia.core.es import Dispatcher
from snakia.core.loader.loader import Loader


class Engine:
    def __init__(self) -> None:
        self.system: Final = System()
        self.dispatcher: Final = Dispatcher()
        self.loader: Final = Loader(self)
        self.__system_thread: threading.Thread | None = None
        self.__dispatcher_thread: threading.Thread | None = None

    def start(self) -> None:
        self.__system_thread = threading.Thread(
            target=self.system.start, daemon=False
        )
        self.__dispatcher_thread = threading.Thread(
            target=self.dispatcher.start, daemon=False
        )
        self.__system_thread.start()
        self.__dispatcher_thread.start()

    def stop(self) -> None:
        if self.__system_thread is not None:
            self.system.stop()
            self.__system_thread.join()
        if self.__dispatcher_thread is not None:
            self.dispatcher.stop()
            self.__dispatcher_thread.join()

    def update(self) -> None:
        self.system.update()
        self.dispatcher.update()
