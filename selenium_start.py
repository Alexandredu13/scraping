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

def wait_css(self, element):
    return self.wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, element)
    ))

def wait_xpath(self, element):
    return self.wait.until(EC.element_to_be_clickable(
        (By.XPATH, element)
    ))

def wait_all_xpath(self, element):
    return self.wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, element)
    ))

def click_js(self, element):
    return self.driver.execute_script("document.querySelector(arguments[0]).click();", element)

