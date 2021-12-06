import logging
import coloredlogs

LOGGER = logging.getLogger(__name__)

def init_logs():
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
    coloredlogs.DEFAULT_LEVEL_STYLES = {
        "warning": {"color": "orange", "bold": True},
        "info": {"color": "green", "bold": True},
        "error": {"color": "red", "bold": True},
    }

    coloredlogs.install(level='DEBUG', logger=LOGGER)

def log_info(message):
    LOGGER.info(f"{message}\n")

def log_error(message):
    LOGGER.error(f"{message}\n")

def log_warn(message):
    LOGGER.warning(f"{message}\n")
