import pygame
import logging

from src.utilities.context import Context

pygame.init()

from src.components.dispatcher import Dispatcher
from src.components.window import Window
from src.components.clock import Clock, TickData
from src.components.stage import Stage

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        logger.info("Initializing process...")
        self.dispatcher = Dispatcher()
        self.window = Window()
        self.clock = Clock()
        self.stage = Stage(Context(window=self.window))
        self.clock.on_tick.connect(self.tick)
        self._attach_quit_handler()

    def _attach_quit_handler(self) -> None:
        logger.debug("Setting up quit event handler.")

        async def _on_quit(event: pygame.event.Event) -> None:
            logger.info("Received QUIT, exiting the process on the next tick...")
            self.quit()

        self.dispatcher.get_signal_for(pygame.QUIT).connect(_on_quit)

    async def tick(self, tick_data: TickData) -> None:
        await self.dispatcher.process_events()

    async def run(self) -> None:
        logger.info("Process ready!")
        await self.clock.run()
        logger.info("Exiting process...")

    def quit(self) -> None:
        logger.info("Stopping process...")
        self.clock.running = False
