# selenium package
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# selenium exceptions
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


path_to_webdriver = "/Users/sashabouloudnine/Desktop/chromedriver"
driver = webdriver.Chrome(path_to_webdriver)
wait = WebDriverWait(driver, 30)

def scroll_to_element(element):
    return driver.execute_script("arguments[0].scrollIntoView();", element)
