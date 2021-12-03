#!/usr/bin/env python3
# script writtin by Coen Stam
# version 2021.12.0

import json
import os
import logging

import timecalc
import webdriver

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

webdriver.open_webpage(url)
webdriver.login_webpage(username, password)

original_date = "2021-12-03"
converted_date = timecalc.convert_date(original_date)

webdriver.open_workorder(converted_date)

start_time = "12.00"
final_start_time = timecalc.time_round_down(*timecalc.split_time(start_time))
logger.debug(f"using starttime: {final_start_time}")

end_time = "22.29"
final_end_time = timecalc.time_round_up(*timecalc.split_time(end_time))
logger.debug(f"using endtime: {final_end_time}")

webdriver.fill_in_form(*final_start_time, *final_end_time)
