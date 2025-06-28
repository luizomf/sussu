import logging
import os

from rich.logging import RichHandler

level_name = os.getenv("SUSSU_LOG_LEVEL", "INFO").upper()
level = getattr(logging, level_name, logging.INFO)

logging.basicConfig(
    level=level,
    format="%(message)s",
    datefmt="[%H:%M]",
    handlers=[
        RichHandler(
            show_time=True,
            show_level=True,
            rich_tracebacks=True,
            omit_repeated_times=False,
            markup=False,
        )
    ],
)

logger = logging.getLogger("rich")
