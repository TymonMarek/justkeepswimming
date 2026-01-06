from dataclasses import dataclass


@dataclass
class LaunchOptions:
    debug: bool = False
    profiler_enabled: bool = False
    profiler_history: int = 1000
