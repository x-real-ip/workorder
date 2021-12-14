import logging
from logging.config import fileConfig

fileConfig("/app/logging.ini")
logger = logging.getLogger(__name__)

logger.info("stopping worker")
