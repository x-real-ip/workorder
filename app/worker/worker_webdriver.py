#!/usr/bin/python3
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import sys

from helper import logging

logger = logging.getLogger(__name__)

# Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(chrome_options=chrome_options)


def open_webpage(url):
    try:
        driver.get(url)
        logger.debug(f"openend: {url}")
    except Exception:
        logger.debug(f"can't open: {url}")


def login_webpage(username, password):
    username_field = driver.find_element(By.TAG_NAME, 'input')
    username_field.send_keys(username)
    next_button = driver.find_element(By.TAG_NAME, 'button')
    next_button.click()
    password_field = driver.find_element(By.TAG_NAME, 'input')
    password_field.send_keys(password)
    login_button = driver.find_element(
        By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[2]/button[2]')
    login_button.click()


def open_workorder(date):
    try:
        order = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
            (By.XPATH, "//div/p[contains(text(),'{}') and preceding-sibling::h6[contains(text(),'dienst') or contains(text(),'Operator') or contains(text(),'motorkap')]]".format(date))))
        order.click()
    except Exception:
        logger.info(f"no workorder was found, closing webdriver")
        driver.quit()
        sys.exit()


def fill_in_form(start_hour, start_minute, end_hour, end_minute):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, '//input[@class="time-input hours"]')))
    start_hours = driver.find_element(
        By.XPATH, '//div[1]/span/input[1][@class="time-input hours"]')
    start_hours.send_keys(Keys.BACKSPACE)
    start_hours.send_keys(start_hour)
    start_minutes = driver.find_element(
        By.XPATH, '//input[2][@class="time-input minutes"]')
    start_minutes.send_keys(start_minute)
    logger.info(f"start time has filled in")
    end_hours = driver.find_element(
        By.XPATH, "//label[contains(text(),'End')]/following-sibling::span/input[@class='time-input hours']")
    end_hours.send_keys(Keys.BACKSPACE)
    end_hours.send_keys(end_hour)
    end_minutes = driver.find_element(
        By.XPATH, "//label[contains(text(),'End')]/following-sibling::span/input[@class='time-input minutes']")
    end_minutes.send_keys(end_minute)
    logger.info(f"end time has filled in")


def send_workorder():
    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * 7)
        actions.send_keys(Keys.ENTER)
        actions.perform()
    except Exception:
        logger.error(
            "workorder was not being send")
        sys.exit()
    else:
        logger.info("workorder send successfully")


def quit():
    driver.quit()
    logger.info("selenium webdrive finished")
