from justkeepswimming.characters.turtle import TurtlePrefab
from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.utilities.scene import Scene


def load() -> Scene:
    scene = Scene(SceneID.DEFAULT)
    MainCameraPrefab().construct(scene)
    TurtlePrefab().construct(scene)
    return scene
