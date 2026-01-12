import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from justkeepswimming.debug.profiler import Profiler
from justkeepswimming.debug.scopes import ProfilerScope


def show(profiler: Profiler) -> None:
    if not profiler.options.enabled:
        return

    processor_records = profiler.records.get(ProfilerScope.PROCESSOR, {})

    _, axis = plt.subplots(2, 2, figsize=(14, 10))  # type: ignore
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    ax_frame = axis[0, 0]
    ax_proc_chart = axis[0, 1]
    ax_mem = axis[1, 0]
    ax_proc_records = axis[1, 1]

    ax_frame.set_title("Frame Time")
    ax_frame.plot(profiler.tick_times_ms, label="Frame Time", color="blue")
    ax_frame.set_ylabel("Milliseconds")
    if profiler.tick_times_ms:
        avg = sum(profiler.tick_times_ms) / len(profiler.tick_times_ms)
        ax_frame.axhline(
            avg, color="red", linestyle="--", label=f"Average ({avg:.2f} ms)"
        )
    ax_frame.legend()

    ax_mem.set_title("Memory Usage")
    ax_mem.plot(
        [memory_usage / (1024 * 1024) for memory_usage in profiler.memory_bytes],
        label="Total Memory Usage",
        color="orange",
    )
    ax_mem.set_ylabel("Megabytes")
    ax_mem.legend()

    # Processor charts
    ax_proc_records.set_title("Processor Times")

    if processor_records:
        # Compute average CPU times and sort descending
        label_value_pairs = []
        for name, times in processor_records.items():
            if times:
                avg = sum(times) / len(times)
            else:
                avg = 0.0
            label_value_pairs.append((name, avg))  # type: ignore

        label_value_pairs.sort(key=lambda x: x[1], reverse=True)  # type: ignore
        labels = [label for label, _ in label_value_pairs]  # type: ignore
        values = [value for fig, value in label_value_pairs]  # type: ignore
        total = sum(values)  # type: ignore

        # Choose a categorical colormap and generate colors matching labels order
        cmap_name = "tab10" if len(labels) <= 10 else "tab20"  # type: ignore
        cmap = plt.get_cmap(cmap_name)
        colors = [cmap(i) for i in range(len(labels))]  # type: ignore

        # Plot time series for each processor using the same order/colors as the pie
        for idx, name in enumerate(labels):  # type: ignore
            times = list(processor_records.get(name, []))  # type: ignore
            if times:
                ax_proc_records.plot(times, label=name, color=colors[idx])
        ax_proc_records.set_xlabel("Tick")
        ax_proc_records.set_ylabel("Milliseconds")

        # Pie chart using the same colors
        if values and total > 0:
            threshold_pct = 15

            def autopct_func(pct: float) -> str:
                return ("%1.1f%%" % pct) if pct >= threshold_pct else ""

            def label_filter(label, value):  # type: ignore
                pct = (value / total) * 100 if total > 0 else 0  # type: ignore
                return label if pct >= threshold_pct else ""  # type: ignore

            # Build time series for each processor in the same order as labels
            times_series = [list(processor_records.get(label, [])) for label in labels]  # type: ignore
            max_len = max((len(t) for t in times_series), default=0)

            # Pad shorter series with zeros so all series have equal length
            for i, series in enumerate(times_series):
                if len(series) < max_len:
                    times_series[i] = series + [0.0] * (max_len - len(series))

            # Replace the earlier line plots with a stacked area chart
            if max_len > 0:
                ax_proc_records.cla()  # clear previous line plots
                x = list(range(max_len))
                ax_proc_records.set_title("Processor CPU Time")
                ax_proc_records.stackplot(x, *times_series, labels=labels, colors=colors)  # type: ignore
                ax_proc_records.set_xlabel("Tick")
                ax_proc_records.set_ylabel("Milliseconds")

            filtered_labels = [  # type: ignore
                label_filter(label, value)  # type: ignore
                for label, value in zip(labels, values)  # type: ignore
            ]

            ax_proc_chart.set_title("Average Processor CPU Time Distribution")
            ax_proc_chart.pie(
                values,
                labels=filtered_labels,
                autopct=autopct_func,
                startangle=90,
                colors=colors,
            )
            ax_proc_chart.axis("equal")
        else:
            ax_proc_chart.set_visible(False)
    else:
        ax_proc_records.set_visible(False)
        ax_proc_chart.set_visible(False)

    plt.show()  # type: ignore


def main() -> None:
    parser = argparse.ArgumentParser(description="Profiler Dump Viewer")
    parser.add_argument(
        "dump_path",
        type=Path,
        help="Path to the profiler data file",
    )

    args = parser.parse_args()
    profiler = Profiler.load(args.dump_path)
    show(profiler)


if __name__ == "__main__":
    main()
