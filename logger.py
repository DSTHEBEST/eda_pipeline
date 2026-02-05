from loguru import logger

logger.add("eda.log", rotation="1 MB")

def get_logger():
    return logger
    