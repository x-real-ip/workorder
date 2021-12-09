# import sqlite3


# con = sqlite3.connect("database.db")
# cur = con.cursor()
# cur.execute(
#     "select * from workdays WHERE date=? ORDER BY id DESC LIMIT 1", ("2021-12-07",))
# result = (cur.fetchall())
# con.close()
# print(result)


#!/usr/bin/env python3
# script writtin by Coen Stam
# version 2021.12.0

import datetime
import os
import logging
from sys import stdout

import app_timecalc
import app_webdriver
from db_query import query

# Logging
logger = logging.getLogger(__name__)
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

logger.info("started script: %s", os.path.abspath(__file__))


# Check os env variables
if "WEB_URL" in os.environ:
    web_url = os.getenv("WEB_URL")
    logger.debug(f"using url: {web_url}")
    if web_url == "URL" or web_url == "":
        logger.error(
            "Please set a correct URL in the prd-workorder-app.env file")
else:
    logger.error(
        "No URL os env find please check prd-workorder-app.env file")

if "WEB_USERNAME" in os.environ:
    web_username = os.getenv("WEB_USERNAME")
    logger.debug(f"using username: {web_username}")
    if web_username == "username" or web_username == "":
        logger.error(
            "Please set a correct username in the prd-workorder-app.env file")
else:
    logger.error(
        "No username os env find please check prd-workorder-app.env file")

if "WEB_PASSWORD" in os.environ:
    web_password = os.getenv("WEB_PASSWORD")
    if web_password == "password" or web_password == "":
        logger.error(
            "Please set a correct password in the prd-workorder-app.env file")
else:
    logger.error(
        "No password os env find please check prd-workorder-app.env file")
