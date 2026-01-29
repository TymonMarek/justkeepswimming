import logging

from justkeepswimming.ecs import Component, Entity, Processor
from justkeepswimming.utilities.scene import Scene


class Prefab:
    extends: "Prefab | list[Prefab] | None" = None
    components: list[Component]
    processors: list[type[Processor]]
    logger = logging.getLogger(__name__)

    def construct(
        self, name: str, scene: "Scene", use_entity: Entity | None = None
    ) -> Entity:
        entity: Entity
        if use_entity is not None:
            entity = use_entity
        else:
            entity = scene.context.create_entity(name)

        if self.extends:
            if isinstance(self.extends, list):
                for prefab in self.extends:
                    prefab.construct(name, scene, use_entity=entity)
            else:
                self.extends.construct(name, scene, use_entity=entity)

        for component in self.components:
            component_type = type(component)
            if entity.has_component(component_type):
                entity.remove_component(entity.get_component(component_type))
            entity.add_component(component.__class__(**vars(component)))

        for processor_cls in self.processors:
            if not any(
                isinstance(processor, processor_cls)
                for processor in scene.scheduler.processors
            ):
                scene.scheduler.add_processor(processor_cls())

        return entity


class PrefabGroup:
    prefabs: dict[str, Prefab]

    def construct(self, name: str, scene: "Scene") -> list[Entity]:
        entities: list[Entity] = []
        for prefab_name, prefab in self.prefabs.items():
            entity = prefab.construct(f"{name}_{prefab_name}", scene)
            entities.append(entity)
        return entities
