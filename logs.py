import logging
import coloredlogs



def init_logs():
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG)
    coloredlogs.DEFAULT_LEVEL_STYLES = {
        "warning": {"color": "orange", "bold": True},
        "success": {"color": "green", "bold": True},
        "error": {"color": "red", "bold": True},
    }

    coloredlogs.install()

def log_info(message):
    logging.info(f"{message}\n")

def log_error(message):
    logging.error(f"{message}\n")

def log_warn(message):
    logging.warning(f"{message}\n")
