import asyncio
import logging
import argparse
from rich.logging import RichHandler

from justkeepswimming.scenes import SceneID
from justkeepswimming.modules.game import Game


def setup_logging(verbosity: int):
    level = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][
        min(3, max(0, verbosity))
    ]
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(show_time=False)],
    )


async def game_loop(enable_dag_visualizer: bool = False):
    game = Game(enable_dag_visualizer=enable_dag_visualizer)
    await game.start()
    await game.stage.switch_scene(SceneID.DEFAULT)
    await game.clock.on_stop.wait()


def main():
    parser = argparse.ArgumentParser(description="Just Keep Swimming")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=1,
        help="Logging verbosity: 0=ERROR, 1=WARNING, 2=INFO, 3=DEBUG",
    )
    parser.add_argument(
        "--debug-dag",
        action="store_true",
        help="Enable DAG visualization debug window",
    )
    args = parser.parse_args()
    setup_logging(args.verbosity)
    asyncio.run(game_loop(enable_dag_visualizer=args.debug_dag))


if __name__ == "__main__":
    main()
