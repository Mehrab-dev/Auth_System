import logging

logger = logging.getLogger(__name__)

file_h = logging.FileHandler('system.log')
file_f = logging.Formatter(" %(asctime)s - %(name)s - %(levelname)s - %(message)s ")
file_h.setFormatter(file_f)
file_h.setLevel(logging.INFO)

logger.addHandler(file_h)
logger.setLevel(logging.INFO)