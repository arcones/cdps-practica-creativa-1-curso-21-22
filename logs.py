import logging


def init_logs():
    LOGGER = logging.getLogger(__name__)
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
    return LOGGER
