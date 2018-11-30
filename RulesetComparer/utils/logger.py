import logging, pytz, os.path
from datetime import datetime
from RulesetComparer.properties.config import *


def initialize_logger():
    log_dir = settings.BASE_DIR + get_file_path("server_log")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.Formatter.converter = local_time

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(log_dir, "error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(log_dir, "debug.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(log_dir, "info.log"), "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logging.debug("initialize logger success")


def local_time(*args):
    utc_dt = datetime.utcnow()
    time_zone = pytz.timezone(TIME_ZONE.get('asia_taipei'))
    converted = utc_dt.astimezone(time_zone)
    return converted.timetuple()
