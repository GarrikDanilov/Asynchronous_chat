import os
import logging
from logging.handlers import TimedRotatingFileHandler


path = os.path.dirname(os.path.abspath(__file__))


logger = logging.getLogger('server')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

log_handler = TimedRotatingFileHandler(os.path.join(path, 'server.log'), encoding='utf-8', 
                                       interval=1, when='D')
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)