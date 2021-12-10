import logging
from sys import stdout

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s")

file_handler = logging.FileHandler("workorder.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
