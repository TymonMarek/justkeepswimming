import time
from collections import deque
from contextlib import contextmanager

import matplotlib.pyplot as plt
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
        processor_records = self.records.get(ProfilerScope.PROCESSOR, {})

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))  # type: ignore
        plt.subplots_adjust(hspace=0.4, wspace=0.3)

        ax_frame = axs[0, 0]
        ax_proc_chart = axs[0, 1]
        ax_mem = axs[1, 0]
        ax_proc_records = axs[1, 1]

        ax_frame.set_title("Frame Time")
        ax_frame.plot(self.tick_times_ms, label="Frame Time", color="blue")
        ax_frame.set_ylabel("Milliseconds")
        if self.tick_times_ms:
            avg = sum(self.tick_times_ms) / len(self.tick_times_ms)
            ax_frame.axhline(
                avg, color="red", linestyle="--", label=f"Average ({avg:.2f} ms)"
            )
        ax_frame.legend()

        ax_mem.set_title("Memory Usage")
        ax_mem.plot(
            [mem / (1024 * 1024) for mem in self.memory_bytes],
            label="Total Memory Usage",
            color="orange",
        )
        ax_mem.set_ylabel("Megabytes")
        ax_mem.legend()

        ax_proc_records.set_title("Processor Times")
        if processor_records:
            for name, times in processor_records.items():
                ax_proc_records.plot(list(times), label=name)
            ax_proc_records.set_xlabel("Tick")
            ax_proc_records.set_ylabel("Milliseconds")
        else:
            ax_proc_records.set_visible(False)

        if processor_records:
            ax_proc_chart.set_title("Processor CPU Time")
            label_value_pairs = []
            for name, times in processor_records.items():
                if times:
                    avg = sum(times) / len(times)
                    label_value_pairs.append((name, avg))  # type: ignore
            label_value_pairs.sort(key=lambda x: x[1], reverse=True)  # type: ignore
            values = [value for _, value in label_value_pairs]  # type: ignore
            labels = [label for label, _ in label_value_pairs]  # type: ignore
            total = sum(values)  # type: ignore
            if values and total > 0:
                threshold_pct = 20

                def autopct_func(pct: float) -> str:
                    return ("%1.1f%%" % pct) if pct >= threshold_pct else ""

                def label_filter(label, value):  # type: ignore
                    pct = (value / total) * 100 if total > 0 else 0  # type: ignore
                    return label if pct >= threshold_pct else ""  # type: ignore

                filtered_labels = [label_filter(label, value) for label, value in zip(labels, values)]  # type: ignore
                ax_proc_chart.pie(
                    values, labels=filtered_labels, autopct=autopct_func, startangle=90
                )
                ax_proc_chart.axis("equal")
            else:
                ax_proc_chart.set_visible(False)
        else:
            ax_proc_chart.set_visible(False)

        plt.show()  # type: ignore
