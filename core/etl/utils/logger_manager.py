import logging
from logging import Logger
import sys
import time

def create_logger(
    name:str, 
    level=logging.INFO, 
    log_file=None
)-> Logger:
    """
    Returns a logger object with the specified name and log level.
    By default, log level is set to INFO.
    You can add a log_file to save logs if needed
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)s] - %(message)s"
    )
    formatter.converter = time.gmtime

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
