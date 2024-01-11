import pathlib
import logging
from logging.handlers import SysLogHandler, RotatingFileHandler


def setup_logging(name: str, log_lvl=logging.WARNING,
                  stream_to_syslog=True, stream_to_screen=True):

    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    logging.getLogger('pika').setLevel(logging.CRITICAL)

    logs_dir = pathlib.Path(__file__).parent.parent.parent / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    name = name.split('.')[-1]
    logs_path = logs_dir / f'{name}.log'

    logging.root.setLevel(log_lvl)

    logging.Formatter.default_msec_format = '%s.%03d'
    format = f'{name} ' \
        '%(levelname)s %(filename)s:%(lineno)d %(funcName)s - %(message)s'

    if stream_to_screen:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(f'%(asctime)s {format}'))
        logging.root.addHandler(stream_handler)

    if stream_to_syslog:
        syslog_handler = SysLogHandler(address='/dev/log')
        syslog_handler.setFormatter(logging.Formatter(format))
        logging.root.addHandler(syslog_handler)

    logger = logging.getLogger(name)
    file_handler = RotatingFileHandler(
        str(logs_path), maxBytes=4 * 1024 * 1024, backupCount=4)
    file_handler.setFormatter(logging.Formatter(f'%(asctime)s {format}'))
    logger.addHandler(file_handler)

    return logger
