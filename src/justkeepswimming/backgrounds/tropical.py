from pathlib import Path

from pygame import Vector2

from justkeepswimming.components.physics import TransformComponent
from justkeepswimming.components.render import RendererComponent
from justkeepswimming.components.tile import (
    AutoTileScrollComponent,
    TileTextureComponent,
)
from justkeepswimming.prefabs.background import MouseParallaxBackgroundLayerPrefab, ScrollingParallaxBackgroundLayerPrefab
from justkeepswimming.utilities.image import Image
from justkeepswimming.utilities.prefab import Prefab, PrefabGroup


class TropicalBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/tropical/1.png"))),
        AutoTileScrollComponent(speed=Vector2(15, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-10),
    ]
    processors = []


class TropicalFishBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/tropical/2.png"))),
        AutoTileScrollComponent(speed=Vector2(50,0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-8),
    ]
    processors = []

class TropicalRocksLayerPrefab(Prefab):
    extends = MouseParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/tropical/3.png"))),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-9),
    ]
    processors = []


class TropicalSandLayerPrefab(Prefab):
    extends = MouseParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/tropical/4.png"))),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-7),
    ]
    processors = []


class TropicalPlantsLayerPrefab(Prefab):
    extends = MouseParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/tropical/5.png"))),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-6),
    ]
    processors = []


class TropicalBackgroundPrefabGroup(PrefabGroup):
    prefabs = {
        "TropicalBackgroundLayerPrefab": TropicalBackgroundLayerPrefab(),
        "TropicalFishBackgroundLayerPrefab": TropicalFishBackgroundLayerPrefab(),
        "TropicalRocksLayerPrefab": TropicalRocksLayerPrefab(),
        "TropicalSandLayerPrefab": TropicalSandLayerPrefab(),
        "TropicalPlantsLayerPrefab": TropicalPlantsLayerPrefab(),
    }
