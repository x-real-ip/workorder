#!/usr/bin/python
# script writtin by Coen Stam
# https://github.com/theautomation
# github@theautomation.nl
# version 2021.12.0

import worker_webdriver
import datetime
import os
import sys

import worker_timecalc

from worker_query import query

import logging
import logging.config

# Path must be absolute because cron runs the script
logging.config.fileConfig("/app/worker/logging.ini",
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def main():

    logger.info("script started")

    # Check os env variables
    if "WEB_URL" in os.environ:
        web_url = os.environ.get("WEB_URL")
        logger.debug(f"using url: {web_url}")
        if web_url == "URL" or web_url == "":
            logger.error(
                "Please set a correct URL in the prd-workorder-app.env file")
            sys.exit()
    else:
        logger.error(
            "No URL os env find please check prd-workorder-app.env file")
        sys.exit()

    if "WEB_USERNAME" in os.environ:
        web_username = os.environ.get("WEB_USERNAME")
        logger.debug(f"using username: {web_username}")
        if web_username == "username" or web_username == "":
            logger.error(
                "Please set a correct username in the prd-workorder-app.env file")
            sys.exit()
    else:
        logger.error(
            "No username os env find please check prd-workorder-app.env file")
        sys.exit()

    if "WEB_PASSWORD" in os.environ:
        web_password = os.environ.get("WEB_PASSWORD")
        if web_password == "password" or web_password == "":
            logger.error(
                "Please set a correct password in the prd-workorder-app.env file")
            sys.exit()
    else:
        logger.error(
            "No password os env find please check prd-workorder-app.env file")
        sys.exit()

    # Get yesterday date as string
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days=1))
    # Use date converter e.g. "2021-01-01 -> "1 Jan"
    converted_date = worker_timecalc.convert_date(yesterday)

    # Query yesterday's time data from database
    try:
        db_query_result = query("/app/db/database.db", yesterday)
        start_time = db_query_result[2]
        end_time = db_query_result[3]
        logger.info(
            f"found worktime in database on day {yesterday}. Start time: {start_time} End time: {end_time}")
    except TypeError as msg:
        logger.warning(f"can't find values in database: {msg}")
        logger.info("exit worker")
        sys.exit()

    # Round down and round up time
    final_start_time = worker_timecalc.time_round_down(
        *worker_timecalc.split_time(start_time))
    logger.info(
        f"using starttime: {final_start_time} for workorder: {converted_date}")

    final_end_time = worker_timecalc.time_round_up(
        *worker_timecalc.split_time(end_time))
    logger.info(
        f"using endtime: {final_end_time} for workorder: {converted_date}")

    # Load webdriver options
    worker_webdriver.setup_driver()

    # Webdriver open URL
    worker_webdriver.open_webpage(web_url)

    # Login with username and password
    worker_webdriver.login_webpage(web_username, web_password)

    # Open workorder that contains converted date if not exists it will exit
    worker_webdriver.open_workorder(converted_date)

    # Fill in time in web form
    worker_webdriver.fill_in_form(*final_start_time, *final_end_time)

    # Click "send"
    worker_webdriver.send_workorder()

    # Quit webdriver
    worker_webdriver.quit()


if __name__ == "__main__":
    main()
