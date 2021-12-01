#!/usr/bin/env python3
# script writtin by Coen Stam
# version 2021.11.1

import json
import os
import logging
import sys
import time
import datetime
from dateutil.relativedelta import relativedelta

import timecalc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s")

file_handler = logging.FileHandler("workorder.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("started script: %s", os.path.abspath(__file__))

## convert date
input_date = "2021-12-01"
date = datetime.datetime.strptime(input_date, "%Y-%m-%d").strftime("%b " "%-d")
logger.debug(f"using date: {date}")

## open external json secrets file to get credentials
secrets_json_filename = (".secrets.json")
secrets_json_path = os.path.abspath(secrets_json_filename)
logger.debug("using secrets from file: %s", secrets_json_path)

try:
  with open(secrets_json_path) as secrets_json:
    objects_secrets_json = json.load(secrets_json)
    secrets_json.close()
except FileNotFoundError as e:
  logger.error(e)

## take objects from secrets.json as variables
username = objects_secrets_json["username"]
password = objects_secrets_json["password"]
url = objects_secrets_json["url"]
logger.debug("variable \"password\" wil not be exposed in this log")
logger.debug(f"variable \"username\" is set to {username}")
logger.debug(f"variable \"url\" is set to: {url}")

## check if default values in secrets.json is changed
if username == "username" or username == "":
  logger.error(f"please enter a valid username in {secrets_json_filename}")
  sys.exit()
if password == "password" or password == "":
  logger.error(f"please enter a valid password in {secrets_json_filename}")
  sys.exit()
if url == "url" or url == "":
  logger.error(f"please enter a valid url in {secrets_json_filename}")
  sys.exit()

## inputvalues
start_time = "09.00"
end_time = "18.15"

timecalc.starttime(start_time)
timecalc.endtime(end_time)

## start selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)

## open webpage
driver.get(url)

## enter username
username_field = driver.find_element(By.TAG_NAME, 'input')
username_field.send_keys(username)

## next
next_button = driver.find_element(By.TAG_NAME, 'button')
next_button.click()

## enter password
password_field = driver.find_element(By.TAG_NAME, 'input')
password_field.send_keys(password)

## login
login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[2]/button[2]')
login_button.click()


## find and open workorder
try:
    order = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div/p[contains(text(),'Dec 1') and preceding-sibling::h6[contains(text(),'motorkap')]]")))
    order.click()
except Exception as e:
    logger.error(e)
    sys.exit()


# ## find and open workorder
# try:
#     order = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[h6[contains(text(),'motorkap')] or h6[contains(text(),'dienst')] and p[contains(text(),'{}')]]".format(today))))
#     order.click()
#     text = order.text.replace("\n", " ")
#     logger.info(f"workorder \"{text}\" selected")
# except Exception as e:
#     logger.error(e)
#     sys.exit()

## wait for order container
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@class="time-input hours"]')))

## enter start time
start_hours = driver.find_element(By.XPATH, '//div[1]/span/input[1][@class="time-input hours"]')
start_hours.send_keys(Keys.BACKSPACE)
start_hours.send_keys(timecalc.starttime.hours)
start_minutes = driver.find_element(By.XPATH, '//input[2][@class="time-input minutes"]')
start_minutes.send_keys(timecalc.starttime.minut)
logger.info(f"start time {start_hours}:{start_minutes} has filled in")

## enter end time
end_hours = driver.find_element(By.XPATH, "//label[contains(text(),'End')]/following-sibling::span/input[@class='time-input hours']")
end_hours.send_keys(Keys.BACKSPACE)
end_hours.send_keys(timecalc.endtime.hours)
end_minutes = driver.find_element(By.XPATH, "//label[contains(text(),'End')]/following-sibling::span/input[@class='time-input minutes']")
end_minutes.send_keys(timecalc.endtime.minut)
logger.info(f"end time {end_hours}:{end_minutes} has filled in")

## tab to the send button because the send button cannot be found with selenium
actions = ActionChains(driver)
actions.send_keys(Keys.TAB * 7)
## enter the submit button because .click() cannot be executed with selenium the reason for this is because the button cannot be found based on XPATH, TAG or TEXT
# actions.send_keys(Keys.ENTER)
## perform the above actions
actions.perform()

## close workorder after send
try:
  close_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[class='button medium primary icon-padding-right']")))
  close_button.click()
except Exception:
  logger.error("workorder was not closed properly and it probably was not sent")
  sys.exit()
else:
  logger.info("workorder completed successfully")

## quit browser
driver.quit()
logger.info("script finished")