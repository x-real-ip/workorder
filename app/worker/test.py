import logging
import logging.config

logging.config.fileConfig("/app/worker/logging.ini")
logger = logging.getLogger(__name__)

logger.info("Test")
