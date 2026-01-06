import time
from collections import deque
from contextlib import contextmanager

import psutil

from justkeepswimming.debug.options import ProfileOptions
from justkeepswimming.debug.scopes import ProfilerScope


class Profiler:
    def __init__(self, enabled: bool, history_length: int):
        self.options = ProfileOptions(
            enabled=enabled,
            history_length=history_length,
        )
        self.records: dict[ProfilerScope, dict[str, deque[float]]] = {}
        self.tick_times_ms: deque[float] = deque(maxlen=self.options.history_length)
        self.memory_bytes: deque[float] = deque(maxlen=self.options.history_length)
        self.process = psutil.Process()

    def record(self, scope: ProfilerScope, name: str, duration: float):
        if scope not in self.records:
            self.records[scope] = {}
        if name not in self.records[scope]:
            self.records[scope][name] = deque(maxlen=self.options.history_length)
        self.records[scope][name].append(duration)

    @contextmanager
    def scope(self, scope: ProfilerScope, name: str):
        if not self.options.enabled:
            yield
            return
        start_time = time.time()
        yield
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        self.record(scope, name, duration)

    @contextmanager
    def measure(self):
        if not self.options.enabled:
            yield
            return
        start_time = time.time()
        yield
        end_time = time.time()
        frame_duration = (end_time - start_time) * 1000
        self.tick_times_ms.append(frame_duration)
        memory_info = self.process.memory_info()
        self.memory_bytes.append(memory_info.rss)

    def show(self) -> None:
        if not self.options.enabled:
            return
        # TODO
