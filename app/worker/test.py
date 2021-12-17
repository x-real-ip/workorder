import logging
import logging.config
import os

logging.config.fileConfig('/app/worker/logging.ini')
logger = logging.getLogger(__name__)

logger.info("Test")

date_filename = ("2021-12-16")

screenshot = os.environ.get('SCREENSHOT', False)
if screenshot == 'True':
    filename = (f"{date_filename}.png")
    print(filename)
