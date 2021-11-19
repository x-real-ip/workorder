#!/usr/bin/env python
# script writtin by Coen Stam
# version 2021.11.1

import json
import os
import sys
import time

# variables
secrets_json_filename = (".secrets.json")

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

# set username and password variables
username = objects_secrets_json["username"]
password = objects_secrets_json["password"]
target_url = objects_secrets_json["target_url"]

# check if default values in secrets.json is changed
if username == "username" or username == "":
  sys.exit("please enter a valid username in", secrets_json_filename)
if password == "password" or password == "":
  sys.exit("please enter a valid password in", secrets_json_filename)

## start selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)

driver.get(target_url)
l = driver.find_element_by_tag_name("input")
l.send_keys("Selenium")