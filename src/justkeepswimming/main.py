import argparse
import asyncio
import logging

from rich.logging import RichHandler

from justkeepswimming.scenes import SceneID
from justkeepswimming.systems.engine import Engine
from justkeepswimming.utilities.launch import LaunchOptions
from justkeepswimming.utilities.logger import logger


def setup_logging(verbosity: int):
    levels: list[int] = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    level = levels[min(3, max(0, verbosity))]
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
        type=int,
        default=1,
        help="Set the verbosity level (0=error, 1=warning, 2=info, 3=debug).",
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
    if args.debug:
        logger.warning("Debug mode is enabled. Performance may be impacted.")
    if args.profiler:
        logger.warning(
            "Profiler is enabled, keeping last %d records.",
            args.profiler_history,
        )
    launch_options = LaunchOptions(
        debug=args.debug,
        profiler_enabled=args.profiler,
        profiler_history=args.profiler_history,
    )
    asyncio.run(game_loop(launch_options))


if __name__ == "__main__":
    main()
