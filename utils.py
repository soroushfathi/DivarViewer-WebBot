from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

IMPORTANT_WAIT= 5
IMPORTANT_TINY_WAIT= 3
DONT_CARE_WAIT= 1000
TINY_WAIT=0.5


def result_items():
    pass


def find_xpath_with_wait(driver, xpath):
    # WebDriverWait(driver, timeout=TINY_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath)))


def find_with_wait2(driver, xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_located_to_be_selected((By.XPATH, xpath)))


def find_with_wait3(driver, xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))


def find_with_wait4(driver, xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.visibility_of_element_located((By.XPATH, xpath)))
