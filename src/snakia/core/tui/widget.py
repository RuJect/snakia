from abc import ABC, abstractmethod
from typing import Final, final

from snakia.core.rx import AsyncBindable, Bindable
from snakia.utils import to_async

from .canvas import Canvas


class Widget(ABC):
    def __init__(self) -> None:
        self.dirty: Final = Bindable(True)
        self.__cache: Canvas = Canvas(0, 0)

    @abstractmethod
    def on_render(self) -> Canvas: ...

    @final
    def render(self) -> Canvas:
        if self.dirty.value:
            result = self.on_render()
            self.__cache = result
            self.dirty.set(False)
        return self.__cache

    @final
    def state[T](self, default_value: T) -> Bindable[T]:
        field = Bindable(default_value)
        field.subscribe(lambda _: self.dirty.set(True))
        return field

    @final
    def async_state[T](self, default_value: T) -> AsyncBindable[T]:
        field = AsyncBindable(default_value)
        field.subscribe(to_async(lambda _: self.dirty.set(True)))
        return field
