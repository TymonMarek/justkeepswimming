# type: ignore
import argparse
import matplotlib.pyplot as plt

from justkeepswimming.debug.profiler import Profiler
from justkeepswimming.debug.scopes import ProfilerScope


def show_summary(profiler: Profiler) -> None:
    """Show full overview: frame time, memory, stacked times and pie."""
    if not profiler.options.enabled:
        return

    processor_records = profiler.records.get(ProfilerScope.PROCESSOR, {})

    fig, axis = plt.subplots(2, 2, figsize=(14, 10))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    ax_frame = axis[0][0]
    ax_proc_chart = axis[0][1]
    ax_mem = axis[1][0]
    ax_proc_records = axis[1][1]

    # Frame time
    ax_frame.set_title("Frame Time")
    ax_frame.plot(profiler.tick_times_ms, label="Frame Time", color="blue")
    ax_frame.set_ylabel("Milliseconds")

    if profiler.tick_times_ms:
        avg_frame = sum(profiler.tick_times_ms) / len(profiler.tick_times_ms)
        ax_frame.axhline(
            avg_frame,
            color="red",
            linestyle="--",
            label=f"Average ({avg_frame:.2f} ms)",
        )
    ax_frame.legend()

    # Memory usage
    ax_mem.set_title("Memory Usage")
    ax_mem.plot(
        [m / (1024 * 1024) for m in profiler.memory_bytes],
        label="Total Memory Usage",
        color="orange",
    )
    ax_mem.set_ylabel("Megabytes")
    ax_mem.legend()

    # Processor times
    ax_proc_records.set_title("Processor Times")

    if processor_records:
        label_value_pairs = []
        for name, pairs in processor_records.items():
            durations = [(end - start) for (start, end) in pairs]
            avg = (sum(durations) / len(durations)) if durations else 0.0
            label_value_pairs.append((name, avg))

        label_value_pairs.sort(key=lambda x: x[1], reverse=True)
        labels = [label for label, _ in label_value_pairs]
        values = [value for _, value in label_value_pairs]
        total = sum(values)

        cmap_name = "tab10" if len(labels) <= 10 else "tab20"
        cmap = plt.get_cmap(cmap_name)
        colors = [cmap(i) for i in range(len(labels))]

        times_series = []
        max_len = 0
        for name in labels:
            durations = [(end - start)
                         for (start, end) in processor_records[name]]
            times_series.append(durations)
            max_len = max(max_len, len(durations))

        padded = [series + [0.0] * (max_len - len(series))
                  for series in times_series]

        if max_len > 0:
            ax_proc_records.cla()
            x = list(range(max_len))
            ax_proc_records.stackplot(x, *padded, labels=labels, colors=colors)
            ax_proc_records.set_title("Processor CPU Time (per tick)")
            ax_proc_records.set_xlabel("Tick")
            ax_proc_records.set_ylabel("Milliseconds")

        if total > 0:
            threshold_pct = 15

            def autopct_func(pct: float) -> str:
                return f"{pct:1.1f}%" if pct >= threshold_pct else ""

            def label_filter(label: str, value: float) -> str:
                pct = 100 * value / total if total > 0 else 0
                return label if pct >= threshold_pct else ""

            filtered_labels = [
                label_filter(
                    label, value) for label, value in zip(
                    labels, values)]

            ax_proc_chart.set_title("Average CPU Time Distribution")
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

    plt.show()


def show_gantt_frame(profiler: Profiler, frame_index: int) -> None:
    """Draw a true start/end Gantt for exactly one frame, labels only inside blocks
    or outside (left/right) when they don't fit. Outside labels are black and
    won't overlap the bar."""
    processor_records = profiler.records.get(ProfilerScope.PROCESSOR, {})
    if not processor_records:
        print("No processor scope records")
        return

    max_len = max(len(pairs) for pairs in processor_records.values())
    if frame_index < 0 or frame_index >= max_len:
        print(f"Frame {frame_index} out of range 0..{max_len - 1}")
        return

    spans = []
    min_start = float("inf")

    for name, pairs in processor_records.items():
        if frame_index < len(pairs):
            start, end = pairs[frame_index]
            spans.append((name, start, end))
            min_start = min(min_start, start)

    spans = [(name, start - min_start, end - min_start)
             for name, start, end in spans]
    if not spans:
        print("No spans for that frame")
        return

    # for placement decisions
    max_end = max(end for _, _, end in spans)

    cmap = plt.get_cmap("tab20")
    colors = {name: cmap(i) for i, name in enumerate({n for n, _, _ in spans})}

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title(f"Frame {frame_index}")
    ax.set_xlabel("Milliseconds")
    ax.set_yticks([])  # no tick labels outside
    ax.set_ylabel("")  # no axis label

    # Draw bars first and keep references
    bar_entries = []
    for idx, (name, start, end) in enumerate(spans):
        width = end - start
        bar = ax.barh(idx, width, left=start,
                      color=colors[name], edgecolor="black")[0]
        bar_entries.append((bar, name, start, end, width))

    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_ylim(-1, len(spans))  # avoid clipping bars
    plt.tight_layout()

    # Ensure the canvas is drawn so we can measure text extents
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    padding_px = 6

    for (bar, name, start, end, width), idx in zip(
        bar_entries, range(len(bar_entries))
    ):
        label = name

        if width > 8:
            ax.text(
                start + width / 2,
                idx,
                label,
                va="center",
                ha="center",
                fontsize=8,
                color="black",
                clip_on=False,
            )
            continue

        # Coordinates in display (pixel) space
        bar_disp_start = ax.transData.transform((start, idx))[0]
        bar_disp_end = ax.transData.transform((end, idx))[0]
        bar_disp_y = ax.transData.transform((end, idx))[1]

        prefer_right = start < (max_end / 2)

        placed = False

        # helper to place text at a display x offset and test overlap
        def try_place_at_disp_x(disp_x: float, ha: str) -> bool:
            data_x = ax.transData.inverted().transform((disp_x, bar_disp_y))[0]
            txt = ax.text(
                data_x,
                idx,
                label,
                va="center",
                ha=ha,
                fontsize=8,
                color="black",
                clip_on=False,
            )
            fig.canvas.draw()
            bbox = txt.get_window_extent(renderer=renderer)
            # check overlap: text bbox should not intrude into bar area
            if bbox.x0 <= bar_disp_end + 1 and ha == "left":
                txt.remove()
                return False
            if bbox.x1 >= bar_disp_start - 1 and ha == "right":
                txt.remove()
                return False
            return True

        # Try preferred side first
        if prefer_right:
            target_disp_x = bar_disp_end + padding_px
            if try_place_at_disp_x(target_disp_x, "left"):
                placed = True
            else:
                # try left side
                target_disp_x = bar_disp_start - padding_px
                if try_place_at_disp_x(target_disp_x, "right"):
                    placed = True
        else:
            target_disp_x = bar_disp_start - padding_px
            if try_place_at_disp_x(target_disp_x, "right"):
                placed = True
            else:
                target_disp_x = bar_disp_end + padding_px
                if try_place_at_disp_x(target_disp_x, "left"):
                    placed = True

        # Fallback: place flush to chart edge (outside) if both sides fail
        if not placed:
            if prefer_right:
                edge_disp_x = ax.transData.transform((max_end, idx))[
                    0] + padding_px
                data_x = ax.transData.inverted().transform(
                    (edge_disp_x, bar_disp_y))[0]
                ax.text(
                    data_x,
                    idx,
                    label,
                    va="center",
                    ha="left",
                    fontsize=8,
                    color="black",
                    clip_on=False,
                )
            else:
                edge_disp_x = ax.transData.transform((0, idx))[0] - padding_px
                data_x = ax.transData.inverted().transform(
                    (edge_disp_x, bar_disp_y))[0]
                ax.text(
                    data_x,
                    idx,
                    label,
                    va="center",
                    ha="right",
                    fontsize=8,
                    color="black",
                    clip_on=False,
                )

    plt.show()


def cli_summary() -> None:
    parser = argparse.ArgumentParser(description="Profiler Summary Viewer")
    parser.add_argument("dump_path", help="Path to .prof dump")
    args = parser.parse_args()

    profiler = Profiler.load(args.dump_path)
    show_summary(profiler)


def cli_frame() -> None:
    parser = argparse.ArgumentParser(description="Profiler Frame Viewer")
    parser.add_argument("dump_path", help="Path to .prof dump")
    parser.add_argument(
        "--frame", "-f", type=int, required=True, help="Frame index to show"
    )
    args = parser.parse_args()

    profiler = Profiler.load(args.dump_path)
    show_gantt_frame(profiler, args.frame)
