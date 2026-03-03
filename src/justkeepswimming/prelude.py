from rich.logging import RichHandler
import logging
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


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
        handlers=[RichHandler(
            show_time=False,
            show_path=True
        )],
    )
