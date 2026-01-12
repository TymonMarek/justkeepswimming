import copy
import logging
from typing import Any

from pygame import Event, Surface, Vector2

from justkeepswimming.ecs import SceneContext
from justkeepswimming.ecs.scheduler import ProcessorScheduler
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.systems.input import InputAction
from justkeepswimming.utilities.context import EngineContext
from justkeepswimming.utilities.signal import Signal

logger = logging.getLogger(__name__)

INTERNAL_RENDER_WINDOW_SIZE = Vector2(1920, 1080)


class Scene:
    def __init__(self, id: SceneID, engine_context: EngineContext) -> None:
        self.id: SceneID = id
        self.context = SceneContext(surface=Surface(INTERNAL_RENDER_WINDOW_SIZE))
        self.scheduler = ProcessorScheduler(engine_context)

        self.actions: list[InputAction] = []

        self.on_load = Signal()
        self.on_enter = Signal[EngineContext]()
        self.on_tick = Signal[TickContext, EngineContext]()
        self.on_exit = Signal[EngineContext]()
        self.on_unload = Signal()

        self.on_enter.connect(self._handle_enter)
        self.on_exit.connect(self._handle_exit)
        self.on_tick.connect(self._process_systems)

    def __deepcopy__(self, memo: dict[int, Any] | None) -> "Scene":
        new_scene = Scene(self.id, self.scheduler.engine_context)
        new_scene.context = copy.deepcopy(self.context, memo)
        new_scene.scheduler = copy.deepcopy(self.scheduler, memo)
        new_scene.actions = copy.deepcopy(self.actions, memo)
        return new_scene

    async def _handle_enter(self, engine_context: EngineContext) -> None:
        for action in self.actions:
            engine_context.input.action_manager.register_action(action)

    async def _handle_exit(self, engine_context: EngineContext) -> None:
        for action in self.actions:
            engine_context.input.action_manager.unregister_action(action)
        self.context.maid.cleanup()

    async def _on_window_resize(self, event: Event) -> None:
        self.context.surface = Surface(Vector2(event.w, event.h))
        logger.debug(f"Scene {self.id} resized to Vector2({event.w}, {event.h})")

    async def _process_systems(
        self, tick_context: TickContext, engine_context: EngineContext
    ) -> None:
        await self.scheduler.process_tick(tick_context, self.context, engine_context)

    def __repr__(self) -> str:
        return self.id.name
