from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from itertools import count
from typing import TYPE_CHECKING, Any, cast, overload

import networkx as nx  # type: ignore

from snakia.utils import nolock

if TYPE_CHECKING:
    from snakia.core.ecs.component import Component
    from snakia.core.ecs.processor import Processor


class System:
    __processors: list[Processor]
    __components: dict[type[Component], set[int]]
    __entitites: dict[int, dict[type[Component], Component]]
    __entity_counter: count[int]
    __dead_entities: set[int]
    __is_running: bool

    def __init__(self) -> None:
        self.__processors = []
        self.__components = defaultdict(set)
        self.__entitites = defaultdict(dict)
        self.__entity_counter = count(start=1)
        self.__dead_entities = set()
        self.__is_running = False

    @property
    def is_running(self) -> bool:
        return self.__is_running

    def full_reset(self) -> None:
        self.__processors = []
        self.__components = defaultdict(set)
        self.__entitites = defaultdict(dict)
        self.__entity_counter = count(start=1)
        self.__dead_entities = set()

    def get_processor[P: Processor](
        self, processor_type: type[P], /
    ) -> P | None:
        for processor in self.__processors:
            if type(processor) is processor_type:
                return processor
        else:
            return None

    def add_processor(self, proccessor: Processor) -> None:
        self.__processors.append(proccessor)
        self._sort_processors()

    def remove_processor(self, processor_type: type[Processor]) -> None:
        for processor in self.__processors:
            if isinstance(processor, processor_type):
                self.__processors.remove(processor)

    @overload
    def get_components[C1: Component](
        self, __c1: type[C1], /
    ) -> Iterable[tuple[int, tuple[C1]]]: ...

    @overload
    def get_components[C1: Component, C2: Component](
        self, __c1: type[C1], __c2: type[C2], /
    ) -> Iterable[tuple[int, tuple[C1, C2]]]: ...

    @overload
    def get_components[C1: Component, C2: Component, C3: Component](
        self, __c1: type[C1], __c2: type[C2], __c3: type[C3], /
    ) -> Iterable[tuple[int, tuple[C1, C2, C3]]]: ...

    @overload
    def get_components[
        C1: Component, C2: Component, C3: Component, C4: Component
    ](
        self, __c1: type[C1], __c2: type[C2], __c3: type[C3], __c4: type[C4], /
    ) -> Iterable[tuple[int, tuple[C1, C2, C3, C4]]]: ...

    @overload
    def get_components[
        C1: Component,
        C2: Component,
        C3: Component,
        C4: Component,
        C5: Component,
    ](
        self,
        __c1: type[C1],
        __c2: type[C2],
        __c3: type[C3],
        __c4: type[C4],
        __c5: type[C5],
        /,
    ) -> Iterable[tuple[int, tuple[C1, C2, C3, C4]]]: ...

    def get_components(
        self, *component_types: type[Component]
    ) -> Iterable[tuple[int, tuple[Component, ...]]]:
        entity_set = set.intersection(
            *(
                self.__components[component_type]
                for component_type in component_types
            )
        )
        for entity in entity_set:
            yield (
                entity,
                tuple(
                    self.__entitites[entity][component_type]
                    for component_type in component_types
                ),
            )

    @overload
    def get_components_of_entity[C1: Component](
        self, entity: int, __c1: type[C1], /
    ) -> tuple[C1 | None]: ...

    @overload
    def get_components_of_entity[C1: Component, C2: Component](
        self, entity: int, __c1: type[C1], __c2: type[C2], /
    ) -> tuple[C1 | None, C2 | None]: ...

    @overload
    def get_components_of_entity[C1: Component, C2: Component, C3: Component](
        self, entity: int, __c1: type[C1], __c2: type[C2], __c3: type[C3], /
    ) -> tuple[C1 | None, C2 | None, C3 | None]: ...

    @overload
    def get_components_of_entity[
        C1: Component,
        C2: Component,
        C3: Component,
        C4: Component,
    ](
        self,
        entity: int,
        __c1: type[C1],
        __c2: type[C2],
        __c3: type[C3],
        __c4: type[C4],
        /,
    ) -> tuple[C1 | None, C2 | None, C3 | None, C4 | None]: ...

    @overload
    def get_components_of_entity[
        C1: Component,
        C2: Component,
        C3: Component,
        C4: Component,
        C5: Component,
    ](
        self,
        entity: int,
        __c1: type[C1],
        __c2: type[C2],
        __c3: type[C3],
        __c4: type[C4],
        __c5: type[C5],
        /,
    ) -> tuple[C1 | None, C2 | None, C3 | None, C4 | None, C5 | None]: ...

    def get_components_of_entity(
        self, entity: int, /, *component_types: type[Component]
    ) -> tuple[Any, ...]:
        entity_dict = self.__entitites[entity]
        return (
            *(
                entity_dict.get(component_type, None)
                for component_type in component_types
            ),
        )

    def get_component[C: Component](
        self, component_type: type[C], /
    ) -> Iterable[tuple[int, C]]:
        for entity in self.__components[component_type].copy():
            yield entity, cast(C, self.__entitites[entity][component_type])

    @overload
    def get_component_of_entity[C: Component](
        self, entity: int, component_type: type[C], /
    ) -> C | None: ...

    @overload
    def get_component_of_entity[C: Component, D: Any](
        self, entity: int, component_type: type[C], /, default: D
    ) -> C | D: ...

    def get_component_of_entity(
        self,
        entity: int,
        component_type: type[Component],
        /,
        default: Any = None,
    ) -> Any:
        return self.__entitites[entity].get(component_type, default)

    def add_component(self, entity: int, component: Component) -> None:
        component_type = type(component)
        self.__components[component_type].add(entity)
        self.__entitites[entity][component_type] = component

    def has_component(
        self, entity: int, component_type: type[Component]
    ) -> bool:
        return component_type in self.__entitites[entity]

    def has_components(
        self, entity: int, *component_types: type[Component]
    ) -> bool:
        components_dict = self.__entitites[entity]
        return all(
            comp_type in components_dict for comp_type in component_types
        )

    def remove_component[C: Component](
        self, entity: int, component_type: type[C]
    ) -> C | None:
        self.__components[component_type].discard(entity)
        if not self.__components[component_type]:
            del self.__components[component_type]
        return cast(C, self.__entitites[entity].pop(component_type))

    def create_entity(self, *components: Component) -> int:
        entity = next(self.__entity_counter)
        if entity not in self.__entitites:
            self.__entitites[entity] = {}
        for component in components:
            component_type = type(component)
            self.__components[component_type].add(entity)
            if component_type not in self.__entitites[entity]:
                self.__entitites[entity][component_type] = component
        return entity

    def delete_entity(self, entity: int, immediate: bool = False) -> None:
        if immediate:
            for component_type in self.__entitites[entity]:
                self.__components[component_type].discard(entity)
                if not self.__components[component_type]:
                    del self.__components[component_type]
            del self.__entitites[entity]
        else:
            self.__dead_entities.add(entity)

    def entity_exists(self, entity: int) -> bool:
        return (
            entity in self.__entitites and entity not in self.__dead_entities
        )

    def start(self) -> None:
        self.__is_running = True
        while self.__is_running:
            self.update()
            nolock()

    def stop(self) -> None:
        self.__is_running = False

    def update(self) -> None:
        self._clear_dead_entities()
        for processor in self.__processors:
            processor.process(self)

    def _clear_dead_entities(self) -> None:
        for entity in self.__dead_entities:
            self.delete_entity(entity, immediate=True)
        self.__dead_entities = set()

    def _sort_processors(self) -> None:
        processors = self.__processors
        G: nx.DiGraph[Processor] = nx.DiGraph()
        for p in processors:
            G.add_node(p)
        for p in processors:
            for after_cls in p.after:
                for q in processors:
                    if isinstance(q, after_cls):
                        G.add_edge(q, p)
            for before_cls in p.before:
                for q in processors:
                    if isinstance(q, before_cls):
                        G.add_edge(p, q)
        sorted_processors = list(nx.topological_sort(G))
        self.__processors = sorted_processors
