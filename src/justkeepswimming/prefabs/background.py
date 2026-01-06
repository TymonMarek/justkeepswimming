from pygame import Vector2

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.position import SceneCenterConstraintComponent
from justkeepswimming.components.sizing import SceneSizeConstraintComponent
from justkeepswimming.components.tile import FitTileSizeToTransformComponent
from justkeepswimming.prefabs.renderable import RenderablePrefab
from justkeepswimming.processors.position import SceneCenterConstraintProcessor
from justkeepswimming.processors.sizing import SceneSizeConstraintProcessor
from justkeepswimming.processors.tile import (
    AutoTileScrollProcessor,
    FitTileSizeToTransformProcessor,
    TileTextureProcessor,
)
from justkeepswimming.utilities.prefab import Prefab


class ScrollingParallaxBackgroundLayerPrefab(Prefab):
    extends = RenderablePrefab()
    components = [
        TransformComponent(
            position=Vector2(0, 0), size=Vector2(0, 0), anchor=Vector2(0, 0)
        ),
        FitTileSizeToTransformComponent(),
        SceneSizeConstraintComponent(),
        SceneCenterConstraintComponent(),
    ]
    processors = [
        TileTextureProcessor,
        AutoTileScrollProcessor,
        FitTileSizeToTransformProcessor,
        SceneSizeConstraintProcessor,
        SceneCenterConstraintProcessor,
    ]
