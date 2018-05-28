# python package
import csv
import time
import random
import sys
import os

# selenium package
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException

# identifiants
email_address = ""
password = ""
sleep_time = 2

# configurer webdriver
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(desired_capabilities=capa)
wait = WebDriverWait(driver, 20)
# driver1 = webdriver.Chrome(desired_capabilities=capa, chrome_options=chrome_options)
# wait1 = WebDriverWait(driver1, 20)

# aller sur la page d accueil
base_url = "https://www.linkedin.com/"
driver.get(base_url)
# driver1.get(base_url)

try:
    wait.until(EC.presence_of_element_located(
                    (By.ID, "login-submit"))
                )
except (TimeoutException):
    sys.exit("Error message - loading page")

# s'identifier
driver.find_element_by_id("login-email").send_keys(email_address)
driver.find_element_by_id("login-password").send_keys(password)
driver.find_element_by_id("login-submit").click()
wait.until(EC.element_to_be_clickable(
    (By.ID, "nav-typeahead-wormhole"))
)

# ouvrir csv
with open('linkedin_items.csv', 'w') as csvfile:
    cwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # creer tableau
    csv_row = []

    # prendre infos
    profils = driver.find_elements_by_css_selector("ul.search-results__list.list-style-none li")
    print(profils[0])
    print(profils[1])
    for profil in profils:
        url_profil = driver.find_element_by_css_selector("a.search-result__result-link.ember-view").get_attribute('href')
        print(url_profil[0])
        print(url_profil[1])
        csv_row.append(url_profil)

        # go url


        # copier dans le csv
        try:
            cwriter.writerow(csv_row)
            print("Row written")
        except(WebDriverException):
            print("Error message - csv")
        finally:
            pass

# fermer les navigateurs
print("Tout est bien la mon pote")
driver.close()
# driver1.close()


