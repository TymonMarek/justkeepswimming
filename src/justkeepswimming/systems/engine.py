import asyncio
import logging
import os
import time

import pygame

from justkeepswimming.debug.profiler import Profiler
from justkeepswimming.scenes import SceneID, default
from justkeepswimming.systems.clock import Clock, TickContext
from justkeepswimming.systems.dispatcher import Dispatcher
from justkeepswimming.systems.input import Input
from justkeepswimming.systems.stage import Stage
from justkeepswimming.systems.window import Window
from justkeepswimming.utilities.context import EngineContext, LaunchOptions

logger = logging.getLogger(__name__)

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
pygame.init()


class Engine:
    def __init__(self, launch_options: LaunchOptions):
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
            launch_options=launch_options,
        )

        self.stage = Stage(
            self.context,
            {
                SceneID.DEFAULT: default.load,
            },
        )

        self._attach_quit_handler()
        self.clock.on_tick.connect(self._process_game)

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
