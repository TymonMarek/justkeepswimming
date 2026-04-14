import enum
import logging
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Optional

from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.scene import Scene, SceneID
from justkeepswimming.utilities.signal import Signal

logger = logging.getLogger(__name__)


class SceneLoadingStrategy(enum.Enum):
    LAZY = enum.auto()
    EAGER = enum.auto()


@dataclass
class StageContext:
    scene: Optional[Scene] = None
    on_request_switch_scene: Signal[[SceneID, bool]] = field(
        default_factory=lambda: Signal[[SceneID, bool]]()
    )


type SceneFactory = Callable[[StageContext, EngineContext], Awaitable[Scene]]


class SceneHandle:
    def __init__(
        self,
        scene_id: SceneID,
        factory: SceneFactory,
        strategy: SceneLoadingStrategy,
    ) -> None:
        self.scene_id = scene_id
        self.factory = factory
        self.strategy = strategy
        self._scene: Optional[Scene] = None

    async def get_scene(
        self, context: StageContext, engine_context: EngineContext
    ) -> Scene:
        self._scene = await self.factory(context, engine_context)
        await self._scene.on_load.emit()
        return self._scene


class Stage:
    def __init__(
        self,
        engine_context: EngineContext,
        scenes: dict[SceneID, SceneFactory],
        loading_strategy: SceneLoadingStrategy = SceneLoadingStrategy.EAGER,
    ) -> None:
        self.scenes = scenes
        self.loading_strategy = loading_strategy
        self.busy = False

        self.scene: Optional[Scene] = None
        self.handles: dict[SceneID, SceneHandle] = {}

        self.on_tick = Signal[TickContext, EngineContext]()
        self.engine_context = engine_context
        self.context = StageContext()

        self.on_tick.connect(self._process_scene)
        self.context.on_request_switch_scene.connect(
            self._handle_request_switch_scene
        )

        if loading_strategy is SceneLoadingStrategy.EAGER:
            self._create_all_handles()

    def _create_all_handles(self) -> None:
        for scene_id, factory in self.scenes.items():
            self.handles[scene_id] = SceneHandle(
                scene_id,
                factory,
                self.loading_strategy,
            )

    def _get_handle(self, scene_id: SceneID) -> SceneHandle:
        try:
            factory = self.scenes[scene_id]
        except KeyError:
            raise ValueError(f"Scene {scene_id} does not exist")

        handle = SceneHandle(scene_id, factory, self.loading_strategy)
        self.handles[scene_id] = handle
        return handle

    async def switch_scene(self, scene_id: SceneID, transition: bool) -> None:
        await self.context.on_request_switch_scene.emit(scene_id, transition)

    async def _handle_request_switch_scene(
        self, scene_id: SceneID, transition: bool
    ) -> None:
        if transition:
            self.engine_context.window.fade(1.0)
            self.busy = True
            self.engine_context.window.reached_target_fade.once(
                lambda: self._transition_scene(scene_id)
            )
        else:
            await self._unload_scene()
            await self._load_scene(scene_id)

    async def _transition_scene(self, scene_id: SceneID) -> None:
        await self._load_scene(scene_id)
        self.engine_context.window.fade(0.0)
        await self.engine_context.window.reached_target_fade.wait()
        self.busy = True

    async def _load_scene(self, scene_id: SceneID) -> None:
        handle = self._get_handle(scene_id)
        self.scene = await handle.get_scene(self.context, self.engine_context)
        await self.scene.on_enter.emit(self.engine_context)

    async def _unload_scene(self) -> None:
        if self.scene:
            self.scene.context.maid.cleanup()
            await self.scene.on_exit.emit(self.engine_context)
            await self.scene.on_unload.emit()

    async def _process_scene(
        self,
        tick_context: TickContext,
        game_context: EngineContext,
    ) -> None:
        if self.scene:
            await self.scene.on_tick.emit(tick_context, game_context)
