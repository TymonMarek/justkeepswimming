import datetime
import pickle
import time
from collections import deque
from contextlib import contextmanager
from pathlib import Path

import psutil

from justkeepswimming.datatypes.version import SemanticVersion
from justkeepswimming.debug.options import ProfileOptions
from justkeepswimming.debug.scopes import ProfilerScope
from justkeepswimming.utilities.logger import logger


class Profiler:
    version = SemanticVersion(2, 0, 0)

    def __init__(self, enabled: bool, history_length: int):
        self.options = ProfileOptions(
            enabled=enabled,
            history_length=history_length,
            dump_path=Path(
                f"dumps/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.prof"
            ),
        )
        self.records: dict[ProfilerScope, dict[str, deque[tuple[float, float]]]] = {}
        self.tick_times_ms: deque[float] = deque(maxlen=self.options.history_length)
        self.memory_bytes: deque[float] = deque(maxlen=self.options.history_length)

    def record(self, scope: ProfilerScope, name: str, start_ms: float, end_ms: float):
        if not self.options.enabled:
            return
        if scope not in self.records:
            self.records[scope] = {}
        if name not in self.records[scope]:
            self.records[scope][name] = deque(maxlen=self.options.history_length)
        self.records[scope][name].append((start_ms, end_ms))

    @contextmanager
    def scope(self, scope: ProfilerScope, name: str):
        if not self.options.enabled:
            yield
            return
        start = time.time() * 1000
        yield
        end = time.time() * 1000
        self.record(scope, name, start, end)

    @contextmanager
    def measure(self):
        if not self.options.enabled:
            yield
            return
        start = time.time()
        yield
        frame = (time.time() - start) * 1000
        if len(self.tick_times_ms) + 1 == self.options.history_length:
            logger.warning("Profiler history is full.")
        self.tick_times_ms.append(frame)
        self.memory_bytes.append(psutil.Process().memory_info().rss)

    def save(self) -> None:
        if not self.options.enabled:
            return
        try:
            self.options.dump_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.options.dump_path, "wb") as file:
                logger.info(
                    f"Saving profiler dump to {self.options.dump_path} (profiler version {self.version})..."
                )
                pickle.dump(self, file)
        except Exception as error:
            logger.error(f"Failed to save profiler dump: {error}")

    @staticmethod
    def load(filename: str) -> "Profiler":
        try:
            with open(filename, "rb") as file:
                profiler = pickle.load(file)
                if not isinstance(profiler, Profiler):
                    raise TypeError(
                        "Failed to load profiler, are you sure this is a valid dump?"
                    )
                if not Profiler.version.is_compatible_with(profiler.version):
                    raise ValueError(
                        f"The profiler dump version {profiler.version} is not compatible with the current version {Profiler.version}."
                    )
                logger.info(
                    f"Loaded profiler dump from {filename} (loaded version {profiler.version}, current version {Profiler.version})"
                )
                return profiler
        except Exception as error:
            logger.error(f"Failed to load profiler dump: {error}")
            raise
