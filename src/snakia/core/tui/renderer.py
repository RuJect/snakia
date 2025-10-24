from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol

from .canvas import Canvas


class RenderTarget(Protocol):
    def write(self, text: str) -> None: ...

    def flush(self) -> None: ...


class Renderer(ABC):
    def __init__(self, target: RenderTarget) -> None:
        self.target = target

    @abstractmethod
    def render(self, canvas: Canvas) -> None:
        pass

    @abstractmethod
    def clear_screen(self) -> None:
        pass

    @abstractmethod
    def hide_cursor(self) -> None:
        pass

    @abstractmethod
    def show_cursor(self) -> None:
        pass

    @abstractmethod
    def set_cursor_position(self, x: int, y: int) -> None:
        pass


class RenderContext:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer
        self._cursor_visible = True

    def __enter__(self) -> RenderContext:
        self.renderer.hide_cursor()
        self.renderer.clear_screen()
        self._cursor_visible = False
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if not self._cursor_visible:
            self.renderer.show_cursor()
        self.renderer.target.flush()

    def render(self, canvas: Canvas) -> None:
        self.renderer.set_cursor_position(0, 0)
        self.renderer.render(canvas)
        self.renderer.target.flush()
