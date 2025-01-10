import logging, sys

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    fmt = '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)

    return logger

logger = get_logger('app-name')

logger.info('This is some common information.')
logger.error('This is an error')
logger.warning('This is a warning')