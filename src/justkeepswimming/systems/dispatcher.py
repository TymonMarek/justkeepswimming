import logging

import pygame
from pygame import Event as PygameEvent

from justkeepswimming.utilities.custom_event import CustomEvent
from justkeepswimming.utilities.signal import Signal

logger = logging.getLogger(__name__)

type EventType = int


class Dispatcher:
    def __init__(self) -> None:
        self.event_signals: dict[EventType, Signal[PygameEvent]] = dict()
        self.custom_events: dict[EventType, CustomEvent] = {}

    def create_event(self) -> CustomEvent:
        event_id = pygame.USEREVENT + len(self.custom_events)
        logger.info(f"Registering custom event type: {event_id}")
        self.custom_events[event_id] = CustomEvent(event_id)
        return self.custom_events[event_id]

    def get_signal_for(self, event_type: EventType) -> Signal[PygameEvent]:
        signal = self.event_signals.get(event_type)
        if signal is None:
            logger.debug(f"Creating signal for event type: {event_type}")
            signal = Signal[PygameEvent]()
            self.event_signals[event_type] = signal
        return self.event_signals[event_type]

    async def _dispatch_event(self, event: PygameEvent) -> None:
        if event.type in self.event_signals:
            signal = self.event_signals[event.type]
            await signal.emit(event)

    async def process_events(self) -> None:
        for event in pygame.event.get():
            await self._dispatch_event(event)
