# script writtin by Coen Stam
# version 2021.12.0

import datetime
import os
import logging
import sys

import worker_timecalc
import worker_webdriver
from worker_query import query
from helper import logging

logger = logging.getLogger(__name__)

logger.info("started script: %s", os.path.abspath(__file__))

# Check os env variables
if "WEB_URL" in os.environ:
    web_url = os.environ.get("WEB_URL")
    logger.debug(f"using url: {web_url}")
    if web_url == "URL" or web_url == "":
        logger.error(
            "Please set a correct URL in the prd-workorder-app.env file")
else:
    logger.error(
        "No URL os env find please check prd-workorder-app.env file")

if "WEB_USERNAME" in os.environ:
    web_username = os.environ.get("WEB_USERNAME")
    logger.debug(f"using username: {web_username}")
    if web_username == "username" or web_username == "":
        logger.error(
            "Please set a correct username in the prd-workorder-app.env file")
else:
    logger.error(
        "No username os env find please check prd-workorder-app.env file")

if "WEB_PASSWORD" in os.environ:
    web_password = os.environ.get("WEB_PASSWORD")
    if web_password == "password" or web_password == "":
        logger.error(
            "Please set a correct password in the prd-workorder-app.env file")
else:
    logger.error(
        "No password os env find please check prd-workorder-app.env file")


# Webdriver open URL
worker_webdriver.open_webpage(web_url)

# Login with username and password
worker_webdriver.login_webpage(web_username, web_password)

# Get yesterday date as string
today = datetime.date.today()
yesterday = str(today - datetime.timedelta(days=1))

# Query yesterday's time data from database
try:
    db_query_result = query("/app/db/database.db", yesterday)
    start_time = db_query_result[2]
    end_time = db_query_result[3]
except TypeError as msg:
    logger.info(f"can't find values in database: {msg}")
    logger.info(f"stopping worker")
    sys.exit()

# Use date converter e.g. "2021-01-01 -> "1 Jan"
converted_date = worker_timecalc.convert_date(yesterday)

# Open workorder that contains converted date if not exists it will exit
worker_webdriver.open_workorder(converted_date)

# Round down and round up time
final_start_time = worker_timecalc.time_round_down(
    *worker_timecalc.split_time(start_time))
logger.debug(f"using starttime: {final_start_time}")

final_end_time = worker_timecalc.time_round_up(
    *worker_timecalc.split_time(end_time))
logger.debug(f"using endtime: {final_end_time}")

# Fill in web form
worker_webdriver.fill_in_form(*final_start_time, *final_end_time)

# # Click "send"
# worker_webdriver.send_workorder()

# # Quit webdriver
# worker_webdriver.quit()
