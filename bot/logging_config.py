import logging
import os
from datetime import datetime

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """
    Configures logging to output to both the console and a file.
    Creates a new log file daily in a 'logs' directory.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"bot_{date_str}.log")
    logger = logging.getLogger("trading_bot")
    logger.setLevel(log_level)
    
    if not logger.handlers:
        c_handler = logging.StreamHandler() 
        f_handler = logging.FileHandler(log_file) 

        c_handler.setLevel(logging.WARNING) 
        f_handler.setLevel(log_level)       
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(log_format)
        f_handler.setFormatter(log_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger

logger = setup_logging()