import logging
import random

from justkeepswimming.backgrounds.oceans import (
    OceanBackgroundPrefabGroup,
)
from justkeepswimming.backgrounds.mines import (
    MinesBackgroundPrefabGroup,
)
from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.prefabs.player import PlayerPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.stage import StageContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.scene import Scene
from justkeepswimming.systems.input import (
    InputAction,
    InputActionId,
    KeyboardKeyType,
)

logger = logging.getLogger(__name__)


async def load(
    stage_context: StageContext, engine_context: EngineContext
) -> Scene:
    scene = Scene(SceneID.MENU, engine_context)
    MainCameraPrefab().construct("MainCamera", scene)
    scene.actions = [
        InputAction(
            InputActionId.PLAYER_MOVE_UP, "Move up", [KeyboardKeyType.W]
        ),
        InputAction(
            InputActionId.PLAYER_TURN_LEFT, "Rotate left", [KeyboardKeyType.Q]
        ),
        InputAction(
            InputActionId.PLAYER_MOVE_DOWN, "Move down", [KeyboardKeyType.S]
        ),
        InputAction(
            InputActionId.PLAYER_TURN_RIGHT,
            "Rotate right",
            [KeyboardKeyType.E],
        ),
        InputAction(
            InputActionId.PLAYER_MOVE_LEFT, "Move left", [KeyboardKeyType.A]
        ),
        InputAction(
            InputActionId.PLAYER_MOVE_RIGHT, "Move right", [KeyboardKeyType.D]
        ),
        go_back_action := InputAction(
            InputActionId.GO_BACK,
            "Go back to the previous scene",
            [KeyboardKeyType.ESCAPE]
        )
    ]

    go_back_action.on_triggered.connect(
        lambda: stage_context.on_request_switch_scene.emit(SceneID.MENU, True)
    )

    PlayerPrefab().construct("Player", scene)
    random.choice(
        [MinesBackgroundPrefabGroup, OceanBackgroundPrefabGroup]
    )().construct("Background", scene)
    return scene
