#!/usr/bin/env python3
# script writtin by Coen Stam
# version 2021.12.0

import datetime
import json
import os
import logging

import app_timecalc
import app_webdriver
from app_query import db_query

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s")

file_handler = logging.FileHandler("workorder.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("started script: %s", os.path.abspath(__file__))

# Open external json secrets file to get credentials
secrets_json_filename = (".secrets.json")
secrets_json_path = os.path.abspath(secrets_json_filename)
logger.debug("using secrets from file: %s", secrets_json_path)

try:
    with open(secrets_json_path) as secrets_json:
        objects_secrets_json = json.load(secrets_json)
        secrets_json.close()
except FileNotFoundError as e:
    logger.error(e)

username = objects_secrets_json["username"]
password = objects_secrets_json["password"]
url = objects_secrets_json["url"]
logger.debug("variable \"password\" wil not be exposed in this log")
logger.debug(f"variable \"username\" is set to {username}")
logger.debug(f"variable \"url\" is set to: {url}")

# Webdriver action
app_webdriver.open_webpage(url)
app_webdriver.login_webpage(username, password)

# Get yesterday date as string
today = datetime.date.today()
yesterday = str(today - datetime.timedelta(days=1))

# Use date converter e.g. "2021-01-01 -> "1 Jan"
converted_date = app_timecalc.convert_date(yesterday)

app_webdriver.open_workorder(converted_date)

# Query yesterday's time data from database
database_name = "workdays.db"
db_query_result = db_query(database_name, yesterday)
start_time = db_query_result[2]
end_time = db_query_result[3]

# Round down and round up time
final_start_time = app_timecalc.time_round_down(
    *app_timecalc.split_time(start_time))
logger.debug(f"using starttime: {final_start_time}")

final_end_time = app_timecalc.time_round_up(*app_timecalc.split_time(end_time))
logger.debug(f"using endtime: {final_end_time}")

app_webdriver.fill_in_form(*final_start_time, *final_end_time)
