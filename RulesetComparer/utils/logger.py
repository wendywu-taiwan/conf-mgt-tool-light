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

    # create warning file handler and set level to warning
    handler = logging.FileHandler(os.path.join(log_dir, "warning.log"), "w")
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create info file handler and set level to info
    handler = logging.FileHandler(os.path.join(log_dir, "info.log"), "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(log_dir, "debug.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def error_log(msg, *args, **kwargs):
    print_log(None, logging.ERROR, msg, *args, **kwargs)


def warning_log(log_class, msg, *args, **kwargs):
    print_log(log_class, logging.WARNING, msg, *args, **kwargs)


def info_log(log_class, msg, *args, **kwargs):
    print_log(log_class, logging.INFO, msg, *args, **kwargs)


def debug_log(log_class, msg, *args, **kwargs):
    print_log(log_class, logging.DEBUG, msg, *args, **kwargs)


def print_log(log_class, level, msg, *args, **kwargs):
    if logging.getLogger().hasHandlers() is False:
        initialize_logger()

    if log_class is not None:
        log_msg = log_class + " :" + msg
    else:
        log_msg = msg

    logging.log(level, log_msg, *args, **kwargs)
    print(log_msg, *args, **kwargs)


def local_time(*args):
    utc_dt = datetime.utcnow()
    time_zone = pytz.timezone(TIME_ZONE.get('asia_taipei'))
    converted = utc_dt.astimezone(time_zone)
    return converted.timetuple()
