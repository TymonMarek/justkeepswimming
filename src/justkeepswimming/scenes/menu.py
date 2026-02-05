from justkeepswimming.backgrounds.tropical import (
    TropicalBackgroundPrefabGroup,
)
from justkeepswimming.prefabs.cameras import (
    MainCameraPrefab
)
from justkeepswimming.prefabs.text import TitleScreenTextPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.stage import StageContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.scene import Scene


async def load(
        stage_context: StageContext,
        engine_context: EngineContext
        ) -> Scene:
    scene = Scene(SceneID.MENU, engine_context)
    MainCameraPrefab().construct("MainCamera", scene)
    TropicalBackgroundPrefabGroup().construct("Background", scene)
    TitleScreenTextPrefab().construct("TitleText", scene)
    return scene
