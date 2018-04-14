# python package
import csv
import time
import random
import sys

# selenium package
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException

# configurer webdriver
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(desired_capabilities=capa)
driver1 = webdriver.Chrome(desired_capabilities=capa)
wait = WebDriverWait(driver, 20)
wait1 = WebDriverWait(driver1, 20)

# aller sur la page d accueil
base_url = "http://www.supremenewyork.com/shop"
driver.get(base_url)

# attendre le chargement
try:
    wait.until(EC.element_to_be_clickable(
                    (By.ID, "shop-scroller"))
                )
except (TimeoutException):
    sys.exit("Error message - loading page")

# ouvrir csv
with open('supreme_items.csv', 'w') as csvfile:
    cwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # ouvrir toutes les pages produits
    products = driver.find_elements_by_xpath("//ul[@id='shop-scroller']/li")
    i = 1
    for product in products:

        # creer tableau
        csv_row = []

        # aller sur la page produit
        url_product = product.find_element_by_css_selector("a").get_attribute('href')
        csv_row.append(url_product)
        print (i)
        print(url_product)
        i = i + 1

        driver1.get(url_product)
        wait1.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "img#img-main"))
                    )

        # PRENDRE LES INFORMATIONS

        # disponibilite
        try:
            driver1.find_element_by_css_selector("b.button.sold-out")
            print("Product " + url_product + " is sold out")
            product_availability = "0"
            csv_row.append(product_availability)

        except(NoSuchElementException):
            print("Product " + url_product + " is available")
            product_availability = "1"
            csv_row.append(product_availability)

        # nom
        try:
            product_name = driver1.find_element_by_css_selector("h1.protect").text.encode('utf-8')
            csv_row.append(product_name)
        except (NoSuchElementException):
            print("Element from " + url_product + " has no name")
        finally:
            pass

        # prix
        try:
            product_price = driver1.find_element_by_css_selector("p.price span").text.encode('utf-8')
            csv_row.append(product_price)
        except (NoSuchElementException):
            print("Element from " + url_product + " has no price")
        finally:
            pass

        # image
        try:
            product_picture = driver1.find_element_by_css_selector("img#img-main").get_attribute('src')
            csv_row.append(product_picture)
        except (NoSuchElementException):
            print("Element from " + url_product + " has no picture")
        finally:
            pass

        # description
        try:
            product_description = driver1.find_element_by_css_selector("p.description").text.encode('utf-8')
            csv_row.append(product_description)
        except (NoSuchElementException):
            print("Element from " + url_product + " has no description")
        finally:
            pass

        # copier dans le csv
        try:
            cwriter.writerow(csv_row)
            print("Row written")

        except(WebDriverException):
            print("Error message - csv")

        finally:
            pass

# fermer les navigateurs
print("Tout est bien la, chef !")
driver.close()
driver1.close()