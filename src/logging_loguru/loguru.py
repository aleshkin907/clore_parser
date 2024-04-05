from loguru import logger
import os


logs_directory = "src/logs"
os.makedirs(logs_directory, exist_ok=True)

logger.add(os.path.join(logs_directory, "debug/debug.log"), rotation="10 MB", level="DEBUG", compression="zip")
logger.add(os.path.join(logs_directory, "info/info.log"), rotation="10 MB", level="INFO", compression="zip")
logger.add(os.path.join(logs_directory, "warning/warning.log"), rotation="10 MB", level="WARNING", compression="zip")
logger.add(os.path.join(logs_directory, "error/error.log"), rotation="10 MB", level="ERROR", compression="zip")
logger.add(os.path.join(logs_directory, "critical/critical.log"), rotation="10 MB", level="CRITICAL", compression="zip")


def get_logger():
    return logger
