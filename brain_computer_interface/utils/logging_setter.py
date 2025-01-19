import logging
from logging.handlers import SysLogHandler, RotatingFileHandler
import pathlib
import platform


def setup_logging(name: str, log_lvl=logging.WARNING,
                  stream_to_syslog=True, stream_to_screen=True):

    # global logger fix settings
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    logging.getLogger('pika').setLevel(logging.CRITICAL)

    # logger init
    name = name.split('.')[-1]
    logger = logging.getLogger(name)
    logger.setLevel(log_lvl)

    # format defining
    logging.Formatter.default_msec_format = '%s.%03d'
    format = f'{name} ' \
        '%(levelname)s %(filename)s:%(lineno)d %(funcName)s - %(message)s'

    # file handler
    logs_dir = pathlib.Path(__file__).parent.parent.parent / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    logs_path = logs_dir / f'{name}.log'
    file_handler = RotatingFileHandler(
        str(logs_path), maxBytes=4 * 1024 * 1024, backupCount=4)
    file_handler.setFormatter(logging.Formatter(f'%(asctime)s {format}'))
    logger.addHandler(file_handler)

    # screen handler
    if stream_to_screen:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(f'%(asctime)s {format}'))
        logger.addHandler(stream_handler)

    # syslog handler
    if stream_to_syslog:
        address = '/var/run/syslog' if platform.system() == 'Darwin' \
            else '/dev/log'
        syslog_handler = SysLogHandler(address=address)
        syslog_handler.setFormatter(logging.Formatter(format))
        logger.addHandler(syslog_handler)

    return logger
