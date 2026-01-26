from pathlib import Path

from pygame import Vector2

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.tile import (
    AutoTileScrollComponent,
    TileTextureComponent,
)
from justkeepswimming.prefabs.background import ScrollingParallaxBackgroundLayerPrefab
from justkeepswimming.utilities.image import Image
from justkeepswimming.utilities.prefab import Prefab, PrefabGroup


class OceanBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/oceans/1.png"))),
        AutoTileScrollComponent(speed=Vector2(45, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-10),
    ]
    processors = []


class OceanSandLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/oceans/2.png"))),
        AutoTileScrollComponent(speed=Vector2(90, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-9),
    ]
    processors = []


class OceanDetailsLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/oceans/3.png"))),
        AutoTileScrollComponent(speed=Vector2(135, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-8),
    ]
    processors = []


class OceanBackgroundPrefabGroup(PrefabGroup):
    prefabs = {
        "OceanBackgroundLayerPrefab": OceanBackgroundLayerPrefab(),
        "OceanSandLayerPrefab": OceanSandLayerPrefab(),
        "OceanDetailsLayerPrefab": OceanDetailsLayerPrefab(),
    }
