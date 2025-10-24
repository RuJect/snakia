from typing import Final, Iterable

from snakia.core.tui import Widget


class ContainerWidget(Widget):
    def __init__(self, children: Iterable[Widget]) -> None:
        super().__init__()
        self.children: Final = self.state([*children])
