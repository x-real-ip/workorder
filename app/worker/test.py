import logging
from logging.config import fileConfig

fileConfig("logging.ini")
logger = logging.getLogger(__name__)

logger.info("stopping worker")
