from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.ecs import Component, Processor
from justkeepswimming.utilities.prefab import Prefab


class GameObjectPrefab(Prefab):
    components: list[Component] = [
        TransformComponent(),
    ]
    processors: list[type[Processor]] = []
