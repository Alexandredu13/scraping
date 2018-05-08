# python package
import csv
import time
import random
import sys
import os
import datetime

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

class ContactManageo():

    def __init__(self):
        self.fieldnames = ['Nom', 'URL', 'Siren', 'Code postal', 'Ville']
        self.client = 'gklein'
        self.date = str(datetime.date.today())
        self.site = 'manageo'
        self.url = 'https://www.manageo.fr/'
        self.cible = 'https://www.manageo.fr/annuaire/95-val-d-oise-syndic-de-copropriete-_dem95-582-1.html'
        self.user_email = 'g.klein.manageo@maildrop.cc'
        self.user_password = 'gklein75'
        self.options = Options()
        self.options.add_argument("--kiosk")
        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome('/Users/sashabouloudnine/Desktop/chromedriver',
                                       desired_capabilities=self.capa, options=self.options)
        self.wait = WebDriverWait(self.driver, 20)

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def connect(self):
        self.driver.get(self.cible)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//img[@id='avatar-connexion']")
        ))
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='fermer-bandeau-cookie-cnil']")
        ))
        cookie_button = self.driver.find_element_by_xpath("//a[@id='fermer-bandeau-cookie-cnil']")
        cookie_button.click()
        avatar = self.driver.find_element_by_xpath("//img[@id='avatar-connexion']")
        avatar.click()
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input#emailLogin")
        ))
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input#passwordLogin")
        ))
        email_area = self.driver.find_element_by_xpath("//input[@id='emailLogin']")
        email_area.click()
        email_area.send_keys(self.user_email)
        password_area = self.driver.find_element_by_xpath("//input[@id='passwordLogin']")
        password_area.click()
        password_area.send_keys(self.user_password)
        button_connect = self.driver.find_element_by_xpath("//button/span[text()='SE CONNECTER']")
        button_connect.click()
        self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//img")
        ))

    def extract(self):
        ContactManageo.connect(self)
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.col-sm-6.col-md-4")
        ))
        items = self.driver.find_elements_by_xpath("//div[@class='col-sm-6 col-md-4']")
        with open('%s_%s_%s.csv' % (self.site, self.client, self.date), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

            for item in items:
                ContactManageo.scroll_to_element(self, item)
                try:
                    nom = item.find_element_by_css_selector('h3.over > a').text
                    nom = nom.strip()
                except NoSuchElementException, Exception.IndexError:
                    nom = ''

                try:
                    url = item.find_element_by_css_selector('h3.over > a').get_attribute('href')
                except NoSuchElementException, Exception.IndexError:
                    url = ''

                try:
                    siren = url.replace('/entreprises/','').replace('.html','')
                except Exception:
                    siren = ''

                try:
                    geoloc = item.find_element_by_css_selector('span.localisation-etablissement-resultats-recherche')
                    geoloc = geoloc.text.strip()
                except NoSuchElementException, Exception.IndexError:
                    geoloc = ''

                if geoloc is not '':
                    geoloc = geoloc.split()
                    cp = geoloc[0]
                    ville = geoloc[1:]
                    ville = ' '.join(ville)
                else:
                    cp = ''
                    ville = ''

                writer.writerow({'Nom': nom, 'URL': url, 'Siren': siren, 'Code postal': cp, 'Ville': ville})
                time.sleep(1)
                print '-- SUCCESS : %s' % nom

        self.driver.close()


contact = ContactManageo()
contact.extract()



