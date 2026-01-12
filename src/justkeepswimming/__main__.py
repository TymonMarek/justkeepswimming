import argparse
import asyncio
import logging

from rich.logging import RichHandler

from justkeepswimming.debug.args import VerbosityAction
from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.engine import Engine
from justkeepswimming.utilities.launch import LaunchOptions


def setup_logging(verbosity: int):
    level = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][
        min(3, max(0, verbosity))
    ]
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(show_time=False)],
    )


async def game_loop(launch_options: LaunchOptions):
    engine = Engine(launch_options)
    await engine.start()
    await engine.stage.switch_scene(SceneID.DEFAULT)
    await engine.clock.on_stop.wait()


def main():
    parser = argparse.ArgumentParser(description="Just Keep Swimming")

    parser.add_argument(
        "-v",
        "--verbose",
        action=VerbosityAction,
        help="Increases the verbosity level (can be specified multiple times).",
        dest="log_level",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode.",
    )
    parser.add_argument(
        "-p",
        "--profiler",
        action="store_true",
        help="Enable the profiler.",
    )
    parser.add_argument(
        "--profiler-history",
        type=int,
        default=1000,
        help="Number of profiler records to keep.",
    )
    args = parser.parse_args()
    setup_logging(args.log_level or 1)
    launch_options = LaunchOptions(
        debug=args.debug,
        profiler_enabled=args.profiler,
        profiler_history=args.profiler_history,
    )
    asyncio.run(game_loop(launch_options))


if __name__ == "__main__":
    main()
