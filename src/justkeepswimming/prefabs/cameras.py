from justkeepswimming.components.render import (
    CameraComponent, MainCameraComponent
)
from justkeepswimming.components.sizing import SceneSizeConstraintComponent
from justkeepswimming.prefabs.physics import GameObjectPrefab
from justkeepswimming.processors.camera import CameraProcessor
from justkeepswimming.processors.render import RendererProcessor
from justkeepswimming.processors.sizing import SceneSizeConstraintProcessor
from justkeepswimming.utilities.prefab import Prefab


class CameraPrefab(Prefab):
    extends = GameObjectPrefab()
    components = [
        CameraComponent(),
    ]
    processors = [
        RendererProcessor,
        CameraProcessor,
    ]


class MainCameraPrefab(Prefab):
    extends = CameraPrefab()
    components = [
        MainCameraComponent(),
        SceneSizeConstraintComponent(),
    ]
    processors = [
        SceneSizeConstraintProcessor,
    ]
