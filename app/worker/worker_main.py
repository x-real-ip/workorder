#!/usr/bin/env python3
#
# script writtin by Coen Stam
# https://github.com/theautomation

import re
import os
import sys
import time
import sqlite3
import datetime
import logging
import logging.config

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

base_path = '/app'
worker_path = base_path + '/worker'
log_path = base_path + '/log'
db_path = base_path + '/db'

env_variables = ('WEB_URL', 'WEB_USERNAME', 'WEB_PASSWORD', 'WORKORDER_WORDS')


logging.config.fileConfig(worker_path + '/logging.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def check_env(var):
    for var in env_variables:
        if var in os.environ:
            if os.environ[var] == "":
                logging.error(f'{var} is empty, please set a value')
                sys.exit()
        else:
            logging.error(
                f'{var} does not exist, please setup this env variable')
            sys.exit()


def query(db_location, date):
    """Return values from database based on date"""
    con = sqlite3.connect(db_location)
    cur = con.cursor()
    cur.execute(
        "select * from workdays WHERE date=? ORDER BY id DESC LIMIT 1", (date,))
    result = (cur.fetchone())
    con.close()
    return result


def convert_date(date_input):
    """Return date as month three letter string and day as non-zero digit. e.g. Jan 1"""
    date_output = datetime.datetime.strptime(
        date_input, "%Y-%m-%d").strftime("%b " "%-d")
    return date_output


def split_time(time):
    """Return time 'HH', 'MM' as list, a non digit character will be used as seperator"""
    time = re.split("\D", time)
    hours = int(time[0])
    minute = int(time[1])
    return [hours, minute]


def time_round_down(hour, minute):
    """Return time 'HH', 'MM' with minutes rounded down to a quarter"""
    if minute <= 15:
        minute = 00
    elif minute <= 30 >= 15:
        minute = 15
    elif minute <= 45 >= 30:
        minute = 30
    else:
        minute = 45
    return (f"{hour:02d}"), (f"{minute:02d}")


def time_round_up(hour, minute):
    """Return time 'HH', 'MM' with minutes rounded up to a quarter"""
    if minute <= 15 >= 00:
        minute = 15
    elif minute <= 30 >= 15:
        minute = 30
    elif minute <= 45 >= 30:
        minute = 45
    else:
        minute = 00
        hour += 1
        if hour == 24:
            hour = 00
    return (f"{hour:02d}"), (f"{minute:02d}")


def main():

    # Check env variables
    check_env(env_variables)

    # Query yesterday's time data from database
    try:
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        db_query_result = query(db_path + '/database.db', yesterday)
        start_time = db_query_result[2]
        end_time = db_query_result[3]
        logger.info(
            f"found worktime in database on day {yesterday} starttime: {start_time} endtime: {end_time}")
    except TypeError:
        logger.info(
            f"can't find any values in the database on day {yesterday}, so there's nothing to do.")
        logger.info("exit worker")
        sys.exit()

    try:
        # Round down and round up time
        final_start_time = time_round_down(*split_time(start_time))
        final_end_time = time_round_up(*split_time(end_time))
        logger.info(
            f"worktime for workorder: {yesterday} is rounded up and down:")
        logger.info(
            f"starttime: {final_start_time[0]}.{final_start_time[1]} endtime: {final_end_time[0]}.{final_end_time[1]}")
    except Exception as msg:
        logger.error(msg)

    # Setup webdriver
    install = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=720,930")
    driver = webdriver.Chrome(service=install, options=options)

    # Open webpage
    try:
        web_url = os.environ.get('WEB_URL')
        driver.get(web_url)
        logger.debug(f"openend: {web_url}")
    except Exception:
        logger.debug(f"can't open: {web_url}")

    # Login
    web_username = os.environ.get('WEB_USERNAME')
    driver.find_element(By.TAG_NAME, 'input').send_keys(web_username)
    driver.find_element(By.TAG_NAME, 'button').click()

    web_password = os.environ.get('WEB_PASSWORD')
    driver.find_element(By.TAG_NAME, 'input').send_keys(web_password)
    driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[2]/button[2]').click()

    # Convert date e.g. "2021-01-01 -> "Jan 1"
    converted_date = convert_date(yesterday)

    # Get word list from env variable
    word_list = os.environ.get('WORKORDER_WORDS').split(", ")

    # Search workorder that contains converted date and a word from word list
    found_word = False
    for word in word_list:
        try:
            order = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//div/p[contains(text(),'{}') and preceding-sibling::h6[contains(text(),'{}')]]".format(converted_date, word))))
            if order != None:
                logger.info(f"found workorder with word: {word}")
                found_word = True
                break
        except:
            logger.debug(
                f"tried to find workorder with word: {word} but was not found")

    # Exit if no workorder is found
    if found_word == False:
        logger.warning("no workorder is found")
        driver.quit()
        logger.info("selenium webdrive finished")
        sys.exit()

    # Open workorder
    order.click()

    # Enter time in workorder
    start_hours = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, '//div[1]/span/input[1][@class="time-input hours"]')))
    start_hours.send_keys(Keys.BACKSPACE)
    start_hours.send_keys(final_start_time[0])

    start_minutes = driver.find_element(
        By.XPATH, '//input[2][@class="time-input minutes"]')
    start_minutes.send_keys(final_start_time[1])

    logger.info(
        f"starttime: {final_start_time[0]}:{final_start_time[1]} has filled in")

    end_hours = driver.find_element(
        By.XPATH, "//label[contains(text(),'End')]/following-sibling::span/input[@class='time-input hours']")
    end_hours.send_keys(Keys.BACKSPACE)
    end_hours.send_keys(final_end_time[0])

    end_minutes = driver.find_element(
        By.XPATH, "//label[contains(text(),'End')]/following-sibling::span/input[@class='time-input minutes']")
    end_minutes.send_keys(final_end_time[1])

    logger.info(
        f"endtime: {final_end_time[0]}:{final_end_time[1]} has filled in")

    # Go to send button
    ActionChains(driver).send_keys(Keys.TAB * 7).perform()
    time.sleep(5)

    # Screenshot
    screenshot = os.environ.get('SAVE_IMAGE', "false")
    if screenshot == "true":
        path = (log_path + '/workorder_' + yesterday + '.png')
        try:
            driver.save_screenshot(path)
            logger.info(
                f"image of entered workorder saved. location: {path}")
        except Exception:
            logger.error("can't save image of workorder")

    # Send
    try:
        ActionChains(driver).send_keys(Keys.ENTER).perform()
    except Exception:
        logger.error("workorder was not being send")
        sys.exit()
    else:
        logger.info("workorder send successfully")

    # Quit webdriver
    driver.quit()
    logger.info("selenium webdrive finished")
    sys.exit()


if __name__ == '__main__':
    main()
