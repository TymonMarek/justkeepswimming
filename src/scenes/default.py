from src.scenes import SceneID
from src.utilities.scene import Scene
from src.systems.render import RenderSystem

def load() -> Scene:
    scene = Scene(SceneID.DEFAULT)
    scene.scheduler.add_system(RenderSystem())
    return scene