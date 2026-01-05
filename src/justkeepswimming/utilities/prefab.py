import logging

from justkeepswimming.ecs import Component, Entity, Processor
from justkeepswimming.utilities.scene import Scene


class Prefab:
    extends: "Prefab | None" = None
    components: list[Component]
    processors: list[type[Processor]]
    logger = logging.getLogger(__name__)

    def construct(self, scene: "Scene") -> Entity:
        if self.extends is not None:
            self.logger.debug(
                "Constructing entity from extended prefab: %s", self.extends
            )
            entity = self.extends.construct(scene)
        else:
            self.logger.debug("Creating new entity from scratch.")
            entity = scene.context.create_entity()

        for component in self.components:
            component_type = type(component)
            self.logger.debug("Adding component: %s", component_type.__name__)

            if entity.has_component(component_type):
                self.logger.debug(
                    "Entity already has component %s, removing it first.",
                    component_type.__name__,
                )
                entity.remove_component(entity.get_component(component_type))

            entity.add_component(component.__class__(**vars(component)))
            self.logger.debug("Component %s added.", component_type.__name__)
        for processor_cls in self.processors:
            if any(isinstance(p, processor_cls) for p in scene.scheduler.processors):
                self.logger.debug(
                    "Processor %s already present in scheduler, skipping.",
                    processor_cls.__name__,
                )
                continue

            self.logger.debug("Adding processor: %s", processor_cls.__name__)
            scene.scheduler.add_processor(processor_cls())

        self.logger.debug("Entity construction complete: %s", entity)
        return entity
