from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.prefabs.player import PlayerPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.stage import StageContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.scene import Scene


async def load(stage_context: StageContext, engine_context: EngineContext) -> Scene:
    scene = Scene(SceneID.DEFAULT)
    MainCameraPrefab().construct(scene)
    PlayerPrefab().construct(scene)
    return scene
