import logging

import pygame

logger = logging.getLogger(__name__)


class CustomEvent:
    def __init__(self, event_type: int) -> None:
        self.event_id: int = event_type

    def dispatch(self) -> None:
        logger.info(f"Dispatching custom event: {self.event_id}")
        pygame.event.post(pygame.event.Event(self.event_id))
