import logging

from rich.logging import RichHandler

logging.basicConfig(
    level="CRITICAL",
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
