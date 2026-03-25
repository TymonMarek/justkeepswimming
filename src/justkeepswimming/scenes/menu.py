import logging

from justkeepswimming.backgrounds.tropical import (
    TropicalBackgroundPrefabGroup,
)
from justkeepswimming.components.ui import ButtonComponent
from justkeepswimming.prefabs.button import PlayButtonPrefab
from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.prefabs.text import TitleScreenTextPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.stage import StageContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.scene import Scene

logger = logging.getLogger(__name__)


async def on_play():
    logger.info("Play button clicked!")


async def on_hover():
    logger.info("Button hovered!")


async def load(stage_context: StageContext, engine_context: EngineContext) -> Scene:
    scene = Scene(SceneID.MENU, engine_context)
    MainCameraPrefab().construct("MainCamera", scene)
    TropicalBackgroundPrefabGroup().construct("Background", scene)
    TitleScreenTextPrefab().construct("TitleText", scene)
    play_button_prefab = PlayButtonPrefab().construct("PlayButton", scene)
    play_button = play_button_prefab.get_component(ButtonComponent)
    play_button.on_click.connect(on_play)
    play_button.on_hover.connect(on_hover)
    return scene
