import logging
import logging.config

logging.config.fileConfig("logging.ini")
logger = logging.getLogger(__name__)

logger.info("Test")
