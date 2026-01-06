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


class FarOceanBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/mines/1.png"))),
        AutoTileScrollComponent(speed=Vector2(90, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-10),
    ]
    processors = []


class FarMinesOceanBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/mines/2.png"))),
        AutoTileScrollComponent(speed=Vector2(180, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-9),
    ]
    processors = []


class FarParticleEffectBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/mines/3.png"))),
        AutoTileScrollComponent(speed=Vector2(270, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-8),
    ]
    processors = []


class NearMinesOceanBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/mines/4.png"))),
        AutoTileScrollComponent(speed=Vector2(360, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-7),
    ]
    processors = []


class NearParticleEffectBackgroundLayerPrefab(Prefab):
    extends = ScrollingParallaxBackgroundLayerPrefab()
    components = [
        TileTextureComponent(Image(Path("assets/backgrounds/mines/5.png"))),
        AutoTileScrollComponent(speed=Vector2(450, 0)),
        TransformComponent(
            position=Vector2(0, 0),
            size=Vector2(0, 0),
            anchor=Vector2(0.0, 0.0),
        ),
        RendererComponent(layer=-6),
    ]
    processors = []


class MinesBackgroundPrefabGroup(PrefabGroup):
    prefabs = {
        "FarOceanBackgroundLayer": FarOceanBackgroundLayerPrefab(),
        "FarMinesOceanBackgroundLayer": FarMinesOceanBackgroundLayerPrefab(),
        "FarParticleEffectBackgroundLayer": FarParticleEffectBackgroundLayerPrefab(),
        "NearMinesOceanBackgroundLayer": NearMinesOceanBackgroundLayerPrefab(),
        "NearParticleEffectBackgroundLayer": NearParticleEffectBackgroundLayerPrefab(),
    }
