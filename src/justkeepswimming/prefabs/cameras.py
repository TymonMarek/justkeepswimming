from justkeepswimming.components.physics import Transform
from justkeepswimming.components.render import Camera, MainCamera
from justkeepswimming.components.sizing import SceneSizeConstraint
from justkeepswimming.ecs import Component, System
from justkeepswimming.systems.camera import CameraSystem
from justkeepswimming.systems.render import RenderSystem
from justkeepswimming.systems.sizing import SceneSizeConstraintSystem
from justkeepswimming.utilities.prefab import Prefab


class CameraPrefab(Prefab):
    components: list[Component] = [
        Camera(),
        Transform(),
    ]
    systems: list[type[System]] = [
        RenderSystem,
        CameraSystem,
    ]


class MainCameraPrefab(Prefab):
    extends = CameraPrefab()
    components: list[Component] = [
        MainCamera(),
        SceneSizeConstraint(),
    ]
    systems: list[type[System]] = [
        SceneSizeConstraintSystem,
    ]
