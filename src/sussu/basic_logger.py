import logging
import os

from rich.logging import RichHandler

level_name = os.getenv("SUSSU_LOG_LEVEL", "INFO").upper()
level = getattr(logging, level_name, logging.INFO)

logger = logging.getLogger("SUSSU")
logger.setLevel(level)

if not logger.hasHandlers():
    handler = RichHandler(
        show_time=True,
        show_level=True,
        rich_tracebacks=False,
        omit_repeated_times=False,
        markup=False,
        enable_link_path=True,
        level=level,
        show_path=True,
    )

    handler.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="[%H:%M]"))
    logger.addHandler(handler)
