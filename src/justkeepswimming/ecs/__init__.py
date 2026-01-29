import logging
from collections.abc import Iterable
from typing import TypeVar, cast, overload

from pygame import Surface, Vector2

from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.maid import Maid
from justkeepswimming.utilities.signal import Signal

logger = logging.getLogger(__name__)

C = TypeVar("C")


class Entity:
    def __init__(self, entity_id: int, name: str,
                 context: "SceneContext") -> None:
        self.id = entity_id
        self.maid = Maid()
        self.name = name
        self.context = context

    def has_component(self, component_type: type["Component"]) -> bool:
        return component_type in self.context.components[self.id]

    def get_component(self, component_type: type[C]) -> C:
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


C1 = TypeVar("C1")
C2 = TypeVar("C2")
C3 = TypeVar("C3")
C4 = TypeVar("C4")

INTERNAL_RENDER_WINDOW_SIZE = Vector2(1920 / 3, 1080 / 3)


class SceneContext:
    def __init__(self) -> None:
        self.time_scale: float = 1
        self.maid: Maid = Maid()
        self.surface: Surface = Surface(INTERNAL_RENDER_WINDOW_SIZE)
        self.entities: dict[int, Entity] = {}
        self.components: dict[int, dict[type, Component]] = {}
        self.on_entity_created = Signal[Entity]()
        self.on_entity_deleted = Signal[Entity]()
        self.on_component_added = Signal[tuple[Entity, Component]]()
        self.on_component_removed = Signal[tuple[Entity, Component]]()
        self._query_cache: dict[tuple[type[Component], ...],
                                list[tuple[Entity, tuple[Component, ...]]]] = {}
        self._query_one_cache: dict[
            tuple[type[Component], ...], tuple[Entity,
                                               tuple[Component, ...]] | None
        ] = {}

    def _invalidate_caches(self) -> None:
        self._query_cache.clear()
        self._query_one_cache.clear()

    def create_entity(self, name: str) -> Entity:
        # This technically won't affect the cache correctness, since no components exist yet for this entity
        # so it is safe to not clear the cache here.
        entity = Entity(len(self.entities) + 1, name, self)
        self.entities[entity.id] = entity
        self.components[entity.id] = {}
        self.on_entity_created.emit_sync(entity)
        return entity

    def delete_entity(self, entity: Entity) -> None:
        if entity.id in self.entities:
            self.on_entity_deleted.emit_sync(entity)
            del self.entities[entity.id]
            del self.components[entity.id]
        self._invalidate_caches()

    def add_component(self, entity: Entity, component: Component) -> None:
        if entity.id not in self.components:
            raise RuntimeError(
                f"Entity {entity.id} does not exist in the scene context."
            )
        for incompatible_component in component.incompatible_with:
            if incompatible_component in self.components[entity.id]:
                raise ValueError(
                    f"Component {
                        type(component).__name__} is incompatible with existing component {
                        incompatible_component.__name__} on entity {
                        entity.id}")
        self.components[entity.id][type(component)] = component
        self.on_component_added.emit_sync((entity, component))
        self._invalidate_caches()

    def remove_component(
            self,
            entity: Entity,
            component_type: type[Component]) -> None:
        if entity.id not in self.components:
            raise RuntimeError(
                f"Entity {entity.id} does not exist in the scene context."
            )
        if component_type in self.components[entity.id]:
            component = self.components[entity.id][component_type]
            del self.components[entity.id][component_type]
            self.on_component_removed.emit_sync((entity, component))
            self._invalidate_caches()

    def get_signal_for_component_addition(
        self, component_type: type[Component], maid: Maid
    ) -> Signal[tuple[Entity, Component]]:
        signal = Signal[tuple[Entity, Component]]()

        async def handler(args: tuple[Entity, Component]) -> None:
            entity, component = args
            if isinstance(component, component_type):
                await signal.emit((entity, component))

        maid.add(self.on_component_added.connect(handler))
        return signal

    def get_signal_for_component_removal(
        self, component_type: type[Component], maid: Maid
    ) -> Signal[tuple[Entity, Component]]:
        signal = Signal[tuple[Entity, Component]]()

        async def handler(args: tuple[Entity, Component]) -> None:
            entity, component = args
            if isinstance(component, component_type):
                await signal.emit((entity, component))

        maid.add(self.on_component_removed.connect(handler))
        return signal

    @overload
    def query(self, component_type: type[C1]
              ) -> Iterable[tuple[Entity, tuple[C1]]]: ...

    @overload
    def query(
        self, first_component_type: type[C1], second_component_type: type[C2]
    ) -> Iterable[tuple[Entity, tuple[C1, C2]]]: ...

    @overload
    def query(
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
    ) -> Iterable[tuple[Entity, tuple[C1, C2, C3]]]: ...

    @overload
    def query(
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
        if self._query_cache.get(classes) is not None:
            yield from self._query_cache[classes]
            return
        results: list[tuple[Entity, tuple[Component, ...]]] = []
        for entity_id, components in self.components.items():
            if all(component_type in components.keys()
                   for component_type in classes):
                entity = self.entities[entity_id]
                components_tuple = tuple(
                    components[component_type] for component_type in classes
                )
                results.append((entity, components_tuple))
                yield (entity, components_tuple)
        self._query_cache[classes] = results

    @overload
    def query_one(
        self, component_type: type[C1]
    ) -> tuple[Entity, tuple[C1]] | None: ...

    @overload
    def query_one(
        self, first_component_type: type[C1], second_component_type: type[C2]
    ) -> tuple[Entity, tuple[C1, C2]] | None: ...

    @overload
    def query_one(
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
    ) -> tuple[Entity, tuple[C1, C2, C3]] | None: ...

    @overload
    def query_one(
        self,
        first_component_type: type[C1],
        second_component_type: type[C2],
        third_component_type: type[C3],
        fourth_component_type: type[C4],
    ) -> tuple[Entity, tuple[C1, C2, C3, C4]] | None: ...

    def query_one(  # type: ignore
        self, *classes: type[Component]
    ) -> tuple[Entity, tuple[Component, ...]] | None:
        if self._query_one_cache.get(classes) is not None:
            return self._query_one_cache[classes]
        for entity_id, components in self.components.items():
            if all(component_type in components.keys()
                   for component_type in classes):
                entity = self.entities[entity_id]
                components_tuple = tuple(
                    components[component_type] for component_type in classes
                )
                self._query_one_cache[classes] = (entity, components_tuple)
                return (entity, components_tuple)
        return None


class Processor:
    writes: frozenset[type[Component]] = frozenset()
    reads: frozenset[type[Component]] = frozenset()
    before: frozenset[type["Processor"]] = frozenset()
    after: frozenset[type["Processor"]] = frozenset()
    alongside: frozenset[type["Processor"]] = frozenset()
    debug_only: bool = False

    def __init__(self) -> None:
        self.maid = Maid()

    def initialize(
        self,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        pass

    def teardown(
        self,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        pass

    async def update(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Processor {self.__class__.__name__}>"
