#!/usr/bin/env python
# script writtin by Coen Stam
# version 2021.11.1

import json
import os
import sys
import time
import logging
from datetime import date
from datetime import timedelta

## logging
logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', filename='workorder.log', level=logging.DEBUG)

logging.info("script started")

## variables
secrets_json_filename = (".secrets.json")


## datetime
today = date.today().strftime("%b " "%d")
yesterday = (date.today() - timedelta(days=1)).strftime("%b " "%d")



# set path variables
dirname = os.path.dirname(__file__)
secrets_json_path = os.path.join(dirname, secrets_json_filename)

## open external json secrets file to get credentials
try:
  with open(secrets_json_path) as secrets_json:
    objects_secrets_json = json.load(secrets_json)
    secrets_json.close()
except FileNotFoundError:
  sys.exit(secrets_json_filename , "not exists in", dirname, "directory")

## take objects from secrets.json as variables
username = objects_secrets_json["username"]
password = objects_secrets_json["password"]
url = objects_secrets_json["url"]

## check if default values in secrets.json is changed
if username == "username" or username == "":
  sys.exit("please enter a valid username in", secrets_json_filename)
if password == "password" or password == "":
  sys.exit("please enter a valid password in", secrets_json_filename)
if url == "url" or url == "":
  sys.exit("please enter a valid password in", secrets_json_filename)

## start selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)
delay = 3

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

## workorder
try:
    order = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'" + today + "')]")))
    print("workorder is found with text", '"' + (order.text) + '"')
    order.click()
except TimeoutException: 
    print("no workorder is found with text", '"' + (order.text) + '"')

logging.info("script finished")