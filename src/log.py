import logging
from logging import handlers
from pathlib import Path
from __main__ import constants


def init() -> None:
    """Set up and configure logging"""
    log_format = logging.Formatter("%(asctime)s || %(name)s || %(levelname)s || %(message)s")

    log_file = Path("logs", "rl_snake.log")
    log_file.parent.mkdir(exist_ok=True)

    file_handler = handlers.RotatingFileHandler(
        log_file,
        maxBytes=3000000,
        backupCount=5
    )
    file_handler.setFormatter(log_format)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG if constants.Misc.debug else logging.INFO)

    root_logger.info("Root logger initilised")
