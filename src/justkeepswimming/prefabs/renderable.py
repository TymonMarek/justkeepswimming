from justkeepswimming.components.render import RendererComponent
from justkeepswimming.prefabs.physics import GameObjectPrefab
from justkeepswimming.processors.render import RendererPreProcessor, RendererProcessor
from justkeepswimming.processors.sizing import RendererTransformConstraintProcessor
from justkeepswimming.utilities.prefab import Prefab


class RenderablePrefab(Prefab):
    extends = GameObjectPrefab()
    components = [RendererComponent()]
    processors = [
        RendererPreProcessor,
        RendererProcessor,
        RendererTransformConstraintProcessor,
    ]
