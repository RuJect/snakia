from typing import Iterable

from snakia.core.tui import Widget
from snakia.core.tui.canvas import Canvas
from snakia.core.tui.char import CanvasChar

from .container import ContainerWidget


class HorizontalSplitWidget(ContainerWidget):
    def __init__(
        self, children: Iterable[Widget], splitter_char: str = "|"
    ) -> None:
        super().__init__(children)
        self.splitter_char = splitter_char

    def on_render(self) -> Canvas:
        children_list = self.children.value
        if not children_list:
            return Canvas(0, 0, CanvasChar())

        child_canvases = [child.render() for child in children_list]
        total_width = (
            sum(canvas.width for canvas in child_canvases)
            + len(child_canvases)
            - 1
        )
        max_height = max(canvas.height for canvas in child_canvases)

        result = Canvas(total_width, max_height, CanvasChar())

        x_offset = 0
        for i, canvas in enumerate(child_canvases):
            result.copy_from(canvas, x_offset, 0)
            x_offset += canvas.width

            if i < len(child_canvases) - 1:
                splitter_char = CanvasChar(self.splitter_char)
                for y in range(max_height):
                    result.set(x_offset, y, splitter_char)
                x_offset += 1

        return result
