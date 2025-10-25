from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from itertools import count
from typing import Any, cast, overload

import networkx as nx  # type: ignore

from snakia.utils import nolock

from .component import Component
from .processor import Processor


class System:
    """
    A system is a collection of entities and components that can be processed by processors.
    """

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
        """Returns True if the system is running."""
        return self.__is_running

    def full_reset(self) -> None:
        """Resets the system to its initial state."""
        self.__processors = []
        self.__components = defaultdict(set)
        self.__entitites = defaultdict(dict)
        self.__entity_counter = count(start=1)
        self.__dead_entities = set()

    def get_processor[P: Processor](
        self, processor_type: type[P], /
    ) -> P | None:
        """Returns the first processor of the given type."""
        for processor in self.__processors:
            if isinstance(processor, processor_type):
                return processor
        return None

    def add_processor(self, proccessor: Processor) -> None:
        """Adds a processor to the system."""
        self.__processors.append(proccessor)
        self._sort_processors()

    def remove_processor(self, processor_type: type[Processor]) -> None:
        """Removes a processor from the system."""
        for processor in self.__processors:
            if isinstance(processor, processor_type):
                self.__processors.remove(processor)

    @overload
    def get_components[T1: Component](
        self, __c1: type[T1], /
    ) -> Iterable[tuple[int, tuple[T1]]]: ...

    @overload
    def get_components[T1: Component, T2: Component](
        self, __c1: type[T1], __c2: type[T2], /
    ) -> Iterable[tuple[int, tuple[T1, T2]]]: ...

    @overload
    def get_components[T1: Component, T2: Component, T3: Component](
        self, __c1: type[T1], __c2: type[T2], __c3: type[T3], /
    ) -> Iterable[tuple[int, tuple[T1, T2, T3]]]: ...

    @overload
    def get_components[
        T1: Component, T2: Component, T3: Component, T4: Component
    ](
        self, __c1: type[T1], __c2: type[T2], __c3: type[T3], __c4: type[T4], /
    ) -> Iterable[tuple[int, tuple[T1, T2, T3, T4]]]: ...

    @overload
    def get_components[
        T1: Component,
        T2: Component,
        T3: Component,
        T4: Component,
        T5: Component,
    ](
        self,
        __c1: type[T1],
        __c2: type[T2],
        __c3: type[T3],
        __c4: type[T4],
        __c5: type[T5],
        /,
    ) -> Iterable[tuple[int, tuple[T1, T2, T3, T4]]]: ...

    def get_components(
        self, *component_types: type[Component]
    ) -> Iterable[tuple[int, tuple[Component, ...]]]:
        """Returns all entities with the given components."""
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
    def get_components_of_entity[T1: Component](
        self, entity: int, __c1: type[T1], /
    ) -> tuple[T1 | None]: ...

    @overload
    def get_components_of_entity[T1: Component, T2: Component](
        self, entity: int, __c1: type[T1], __c2: type[T2], /
    ) -> tuple[T1 | None, T2 | None]: ...

    @overload
    def get_components_of_entity[T1: Component, T2: Component, T3: Component](
        self, entity: int, __c1: type[T1], __c2: type[T2], __c3: type[T3], /
    ) -> tuple[T1 | None, T2 | None, T3 | None]: ...

    @overload
    def get_components_of_entity[
        T1: Component,
        T2: Component,
        T3: Component,
        T4: Component,
    ](
        self,
        entity: int,
        __c1: type[T1],
        __c2: type[T2],
        __c3: type[T3],
        __c4: type[T4],
        /,
    ) -> tuple[T1 | None, T2 | None, T3 | None, T4 | None]: ...

    @overload
    def get_components_of_entity[
        T1: Component,
        T2: Component,
        T3: Component,
        T4: Component,
        C5: Component,
    ](
        self,
        entity: int,
        __c1: type[T1],
        __c2: type[T2],
        __c3: type[T3],
        __c4: type[T4],
        __c5: type[C5],
        /,
    ) -> tuple[T1 | None, T2 | None, T3 | None, T4 | None, C5 | None]: ...

    def get_components_of_entity(
        self, entity: int, /, *component_types: type[Component]
    ) -> tuple[Any, ...]:
        """Returns the components of the given entity."""
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
        """Returns all entities with the given component."""
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
        """Returns the component of the given entity."""
        return self.__entitites[entity].get(component_type, default)

    def add_component(self, entity: int, component: Component) -> None:
        """Adds a component to an entity."""
        component_type = type(component)
        self.__components[component_type].add(entity)
        self.__entitites[entity][component_type] = component

    def has_component(
        self, entity: int, component_type: type[Component]
    ) -> bool:
        """Returns True if the entity has the given component."""
        return component_type in self.__entitites[entity]

    def has_components(
        self, entity: int, *component_types: type[Component]
    ) -> bool:
        """Returns True if the entity has all the given components."""
        components_dict = self.__entitites[entity]
        return all(
            comp_type in components_dict for comp_type in component_types
        )

    def remove_component[C: Component](
        self, entity: int, component_type: type[C]
    ) -> C | None:
        """Removes a component from an entity."""
        self.__components[component_type].discard(entity)
        if not self.__components[component_type]:
            del self.__components[component_type]
        return self.__entitites[entity].pop(component_type)  # type: ignore

    def create_entity(self, *components: Component) -> int:
        """Creates an entity with the given components."""
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
        """Deletes an entity."""
        if immediate:
            for component_type in self.__entitites[entity]:
                self.__components[component_type].discard(entity)
                if not self.__components[component_type]:
                    del self.__components[component_type]
            del self.__entitites[entity]
        else:
            self.__dead_entities.add(entity)

    def entity_exists(self, entity: int) -> bool:
        """Returns True if the entity exists."""
        return (
            entity in self.__entitites and entity not in self.__dead_entities
        )

    def start(self) -> None:
        """Starts the system."""
        self.__is_running = True
        while self.__is_running:
            self.update()
            nolock()

    def stop(self) -> None:
        """Stops the system."""
        self.__is_running = False

    def update(self) -> None:
        """Updates the system."""
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
