from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.prefabs.sprites import SpritePrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.utilities.scene import Scene


def load() -> Scene:
    scene = Scene(SceneID.DEFAULT)
    MainCameraPrefab().construct(scene)
    SpritePrefab().construct(scene)
    return scene
