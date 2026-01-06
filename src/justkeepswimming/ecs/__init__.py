import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import cast, overload

from pygame import Surface, Vector2

from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.maid import Maid

logger = logging.getLogger(__name__)


class Entity:
    def __init__(self, entity_id: int, name: str, context: "SceneContext") -> None:
        self.id = entity_id
        self.name = name
        self.context = context

    def has_component(self, component_type: type["Component"]) -> bool:
        return component_type in self.context.components[self.id]

    def get_component[C](self, component_type: type[C]) -> C:
        return cast(C, self.context.components[self.id][component_type])

    def add_component(self, component: "Component") -> None:
        self.context.add_component(self, component)

    def remove_component(self, component: "Component") -> None:
        if self.has_component(type(component)):
            del self.context.components[self.id][type(component)]

    def __repr__(self) -> str:
        return f"<Entity {self.name} ({self.id})>"


class Component:
    incompatible_with: frozenset[type["Component"]] = frozenset()
    pass


@dataclass
class SceneContext:
    maid: Maid = field(default_factory=Maid)
    surface: Surface = field(default_factory=lambda: Surface(Vector2(0, 0)))
    entities: dict[int, Entity] = field(default_factory=dict[int, Entity])
    components: dict[int, dict[type, Component]] = field(
        default_factory=dict[int, dict[type, Component]]
    )

    def create_entity(self, name: str) -> Entity:
        entity = Entity(len(self.entities) + 1, name, self)
        self.entities[entity.id] = entity
        self.components[entity.id] = {}
        return entity

    def delete_entity(self, entity: Entity) -> None:
        if entity.id in self.entities:
            del self.entities[entity.id]
            del self.components[entity.id]

    def add_component(self, entity: Entity, component: Component) -> None:
        if entity.id in self.components:
            for incompatible_component in component.incompatible_with:
                if incompatible_component in self.components[entity.id]:
                    raise ValueError(
                        f"Component {
                            type(component).__name__} is incompatible with existing component {
                            incompatible_component.__name__} on entity {
                            entity.id}"
                    )
            self.components[entity.id][type(component)] = component

    @overload
    def query[
        C1
    ](self, component_type: type[C1]) -> Iterable[tuple[Entity, tuple[C1]]]: ...

    @overload
    def query[
        C1, C2
    ](
        self, first_component_type: type[C1], second_component_type: type[C2]
    ) -> Iterable[tuple[Entity, tuple[C1, C2]]]: ...

    @overload
    def query[
        C1, C2, C3
    ](
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
    ) -> Iterable[tuple[Entity, tuple[C1, C2, C3]]]: ...

    @overload
    def query[
        C1, C2, C3, C4
    ](
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
        fourth_component_type: type[C4],
    ) -> Iterable[tuple[Entity, tuple[C1, C2, C3, C4]]]: ...

    # https://discuss.python.org/t/pre-pep-considerations-and-feedback-type-transformations-on-variadic-generics/50605
    def query(  # type: ignore
        self, *classes: type[Component]
    ) -> Iterable[tuple[Entity, tuple[Component, ...]]]:
        for entity_id, components in self.components.items():
            if all(component_type in components.keys() for component_type in classes):
                entity = self.entities[entity_id]
                components_tuple = tuple(
                    components[component_type] for component_type in classes
                )
                yield (entity, components_tuple)

    @overload
    def query_one[
        C1
    ](self, component_type: type[C1]) -> tuple[Entity, tuple[C1]] | None: ...

    @overload
    def query_one[
        C1, C2
    ](self, first_component_type: type[C1], second_component_type: type[C2]) -> (
        tuple[Entity, tuple[C1, C2]] | None
    ): ...

    @overload
    def query_one[
        C1, C2, C3
    ](
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
    ) -> (tuple[Entity, tuple[C1, C2, C3]] | None): ...

    @overload
    def query_one[
        C1, C2, C3, C4
    ](
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
        fourth_component_type: type[C4],
    ) -> (tuple[Entity, tuple[C1, C2, C3, C4]] | None): ...

    def query_one(  # type: ignore
        self, *classes: type[Component]
    ) -> tuple[Entity, tuple[Component, ...]] | None:
        for entity_id, components in self.components.items():
            if all(component_type in components.keys() for component_type in classes):
                entity = self.entities[entity_id]
                components_tuple = tuple(
                    components[component_type] for component_type in classes
                )
                return (entity, components_tuple)
        return None


class Processor:
    writes: frozenset[type[Component]] = frozenset()
    reads: frozenset[type[Component]] = frozenset()
    before: frozenset[type["Processor"]] = frozenset()
    after: frozenset[type["Processor"]] = frozenset()
    alongside: frozenset[type["Processor"]] = frozenset()

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Processor {self.__class__.__name__}>"
