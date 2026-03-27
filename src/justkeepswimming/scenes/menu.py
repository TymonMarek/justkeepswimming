import logging

from justkeepswimming.backgrounds.tropical import (
    TropicalBackgroundPrefabGroup,
)
from justkeepswimming.components.ui import ButtonComponent
from justkeepswimming.prefabs.button import PlayButtonPrefab, QuitButtonPrefab, SettingsButtonPrefab
from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.prefabs.text import TitleScreenTextPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.stage import StageContext
from justkeepswimming.utilities.context import CustomEventType, EngineContext
from justkeepswimming.utilities.scene import Scene

logger = logging.getLogger(__name__)


async def load(stage_context: StageContext, engine_context: EngineContext) -> Scene:
    scene = Scene(SceneID.MENU, engine_context)
    MainCameraPrefab().construct("MainCamera", scene)
    TropicalBackgroundPrefabGroup().construct("Background", scene)
    TitleScreenTextPrefab().construct("TitleText", scene)
    PlayButtonPrefab().construct("PlayButton", scene)
    SettingsButtonPrefab().construct("SettingsButton", scene)
    quit_button_prefab = QuitButtonPrefab().construct("QuitButton", scene)
    
    async def on_quit_button_click():
        logger.info("Exiting game...")
        engine_context.custom_events[CustomEventType.QUIT].dispatch()

    quit_button_prefab.get_component(ButtonComponent).on_click.connect(on_quit_button_click)
    return scene
