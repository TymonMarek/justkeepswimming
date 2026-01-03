import asyncio

import os

from justkeepswimming.scenes import SceneID, default

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
from logging import getLogger

from justkeepswimming.utilities.context import GameContext

pygame.init()

from justkeepswimming.modules.dispatcher import Dispatcher
from justkeepswimming.modules.window import Window
from justkeepswimming.modules.clock import Clock, TickContext
from justkeepswimming.modules.stage import Stage


class Game:
    def __init__(self, enable_dag_visualizer: bool = False):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing process...")
        self.dispatcher = Dispatcher()
        self.window = Window(self.dispatcher)
        self.clock = Clock()

        self.context = GameContext(
            clock=self.clock,
            window=self.window,
            dispatcher=self.dispatcher,
        )

        # Initialize DAG visualizer if enabled
        self.dag_visualizer = None
        if enable_dag_visualizer:
            from justkeepswimming.utilities.dag_visualizer import DAGVisualizer

            self.dag_visualizer = DAGVisualizer()
            self.logger.info("DAG visualizer enabled")

        self.stage = Stage(
            self.context,
            {
                SceneID.DEFAULT: default.load,
            },
            dag_visualizer=self.dag_visualizer,
        )

        self._attach_quit_handler()
        self.clock.on_tick.connect(self._process_game)

    def _attach_quit_handler(self) -> None:
        self.logger.debug("Setting up quit event handler.")

        async def _on_quit(event: pygame.event.Event) -> None:
            self.logger.info("Received QUIT, exiting the process on the next tick...")
            await self._quit()

        self.dispatcher.get_signal_for(pygame.QUIT).connect(_on_quit)

    async def _process_game(self, tick_context: TickContext) -> None:
        await self.dispatcher.process_events()
        await self.stage.on_tick.emit(tick_context, self.context)

    async def start(self) -> None:
        self.logger.info("Process ready!")

        # Start DAG visualizer if enabled
        if self.dag_visualizer:
            self.dag_visualizer.start()

        asyncio.create_task(self.clock.on_start.emit())
        self.logger.info("Exiting process...")

    async def _quit(self) -> None:
        self.logger.info("Stopping process...")

        # Stop DAG visualizer if running
        if self.dag_visualizer:
            self.dag_visualizer.stop()

        await self.clock.on_stop.emit()
