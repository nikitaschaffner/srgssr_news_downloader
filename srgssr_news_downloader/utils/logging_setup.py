import logging
import sys

def setup_logger() -> object:
    """Set up a logger that writes a log file.

    Returns:
        logger Object
    """
    logger = logging.getLogger("news_downloader")
    fh = logging.FileHandler("output_log.txt")
    ch = logging.StreamHandler()

    level = logging.INFO
    if "--DEBUG" in sys.argv: 
        level = logging.DEBUG

    logger.setLevel(level)   
    fh.setLevel(level)  
    ch.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

# Initialize the logger
logger = setup_logger()