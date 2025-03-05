import os
import logging

"""
Configures logging to a common log file.
"""

def setup_logger(log_file=None) -> logging.Logger:
    """
    Set up a logger that always writes to a common log file.
    If no log_file is provided, it will be created in the 'logs' folder in the project root.
    This ensures that regardless of which file is run, the same log file is used.
    """

    logger = logging.getLogger("geoloc_util")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    if log_file is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        logs_dir = os.path.join(project_root, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, "geoloc_util.log")

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
