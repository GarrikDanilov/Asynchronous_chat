import os
import logging


path = os.path.dirname(os.path.abspath(__file__))


logger = logging.getLogger('client')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

log_handler = logging.FileHandler(os.path.join(path, 'client.log'), encoding='utf-8')
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)