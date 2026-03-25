import asyncio
import logging
import time

import pygame

from justkeepswimming.debug.profiler import Profiler
from justkeepswimming.scenes import SceneID, menu
from justkeepswimming.systems.clock import Clock, TickContext
from justkeepswimming.systems.dispatcher import Dispatcher
from justkeepswimming.systems.input import (
    Input,
    InputAction,
    InputActionId,
    KeyboardKeyType,
)
from justkeepswimming.systems.stage import Stage
from justkeepswimming.systems.window import Window
from justkeepswimming.utilities.context import EngineContext, Options

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, launch_options: Options):
        self.time_started = time.time()
        logger.info("Initializing...")
        self.dispatcher = Dispatcher()
        self.window = Window(self.dispatcher)
        self.input = Input(self.dispatcher)
        self.profiler = Profiler(
            launch_options.profiler_enabled, launch_options.profiler_history
        )
        self.clock = Clock(self.profiler)

        self.context = EngineContext(
            clock=self.clock,
            window=self.window,
            dispatcher=self.dispatcher,
            input=self.input,
            profiler=self.profiler,
            options=launch_options,
        )

        self.stage = Stage(
            self.context,
            {
                SceneID.MENU: menu.load,
            },
        )

        self._attach_quit_handler()
        self._attach_debug_action()
        self.clock.on_tick.connect(self._process_game)
        self.clock.on_stop.connect(self.__profiler_save_dump)

    async def _toggle_debug_mode(self) -> None:
        self.context.options.debug = not self.context.options.debug
        logger.warning(
            f"Debug mode {'enabled' if self.context.options.debug else 'disabled'}!"
        )

    def _attach_debug_action(self) -> None:
        debug_action = InputAction(
            InputActionId.TOGGLE_DEBUG_MODE, "Toggle Debug Mode", [KeyboardKeyType.F3]
        )
        self.input.action_manager.register_action(debug_action)
        debug_action.on_triggered.connect(self._toggle_debug_mode)

    async def __profiler_save_dump(self) -> None:
        self.profiler.save()

    def _attach_quit_handler(self) -> None:
        async def _on_quit(_: pygame.event.Event) -> None:
            await self._quit()

        self.dispatcher.get_signal_for(pygame.QUIT).connect(_on_quit)

    async def _process_game(self, tick_context: TickContext) -> None:
        await self.dispatcher.process_events()
        await self.stage.on_tick.emit(tick_context, self.context)

    async def start(self) -> None:
        asyncio.create_task(self.clock.on_start.emit())
        seconds = time.time() - self.time_started
        logger.info(f"Ready in {seconds:.2f} seconds!")

    async def _quit(self) -> None:
        logger.info("Stopping...")
        await self.clock.on_stop.emit()
