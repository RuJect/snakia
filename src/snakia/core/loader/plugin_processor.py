from __future__ import annotations

from typing import Final, final

from snakia.core.ecs import Processor

from .plugin import Plugin


class PluginProcessor(Processor):
    @final
    def __init__(self, plugin: Plugin) -> None:
        self.plugin: Final = plugin
