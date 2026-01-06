from justkeepswimming.characters.turtle import TurtlePrefab
from justkeepswimming.prefabs.cameras import MainCameraPrefab
from justkeepswimming.prefabs.player import PlayerPrefab
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.input import InputAction, InputActionId, KeyboardKeyType
from justkeepswimming.systems.stage import StageContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.scene import Scene


async def load(stage_context: StageContext, engine_context: EngineContext) -> Scene:
    scene = Scene(SceneID.DEFAULT)
    MainCameraPrefab().construct(scene)
    TurtlePrefab().construct(scene)
    scene.actions = [
        InputAction(InputActionId.PLAYER_MOVE_UP, "Move up", [KeyboardKeyType.W]),
        InputAction(InputActionId.PLAYER_MOVE_DOWN, "Move down", [KeyboardKeyType.S]),
        InputAction(InputActionId.PLAYER_MOVE_LEFT, "Move left", [KeyboardKeyType.A]),
        InputAction(InputActionId.PLAYER_MOVE_RIGHT, "Move right", [KeyboardKeyType.D]),
    ]
    PlayerPrefab().construct(scene)
    return scene
