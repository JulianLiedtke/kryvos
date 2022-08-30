import logging
from os.path import join

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


logging_setup_done = False


def setup_logging():
    global logging_setup_done
    if logging_setup_done:
        return
    logging_setup_done = True
    root = logging.getLogger()
    root.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(LOG_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root.addHandler(stream_handler)
