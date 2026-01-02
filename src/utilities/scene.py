from logging import getLogger

from src.scenes import SceneID
from src.modules.clock import TickContext
from src.ecs.scheduler import SystemScheduler
from src.utilities.context import GameContext
from src.ecs import SceneContext
from src.utilities.signal import Signal


class Scene:
    def __init__(self, id: SceneID):
        self.id: SceneID = id
        self.logger = getLogger(__name__)
        self.context = SceneContext()
        self.scheduler = SystemScheduler()
        self.on_load = Signal()
        self.on_enter = Signal()
        self.on_tick = Signal[TickContext, GameContext]()
        self.on_exit = Signal()
        self.on_unload = Signal()
        self.on_tick.connect(self._process_systems)
        
    async def _process_systems(self, tick_context: TickContext, engine_context: GameContext) -> None:
        await self.scheduler.process_tick(tick_context, self.context, engine_context)

    def __repr__(self) -> str:
        return self.id.name
