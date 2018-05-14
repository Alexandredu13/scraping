# python package
import csv
import time
import random
import codecs

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


class SeleniumOiko:
    def __init__(self):
        self.path_to_webdriver = "/Users/sashabouloudnine/Desktop/chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--kiosk")
        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(self.path_to_webdriver, desired_capabilities=self.capa,
                                       chrome_options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url1 = "https://extranet.axelliance-solution.com/Account/Login"
        self.url2 = "https://extranet.axelliance-solution.com/Tarifer"
        self.url3 = "https://extranet.axelliance-solution.com/Tarifer/Gamme/5"

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

    def scroll_to_element(self, element):
        return self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_js(self, element):
        return self.driver.execute_script("document.querySelector(arguments[0]).click();", element)

    def connect(self):
        self.driver.get(self.url1)
        identifiant = spider.wait_css("input#Login")
        password = spider.wait_css("input#Password")
        identifiant.send_keys("09051123")
        password.send_keys("cUMZg6AYZ478tt28")
        buttonOne = spider.wait_css("button.btn.btn-login.submit-button")
        buttonOne.click()
        print('Connecté à : %s' % self.url2)

    def extract(self):
        SeleniumOiko.connect(self)
        sante_bloc = spider.wait_xpath("//h4[text()='Santé et Prévoyance TNS']")
        sante_bloc.click()
        print('Connecté à : %s' % self.url3)
        urlPrevoyance = spider.wait_css("a#url-tarificateur-42")
        #urlSante = SeleniumOiko.wait_css("a#url-tarificateur-43")
        urlPrevoyance.click()
        form = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.content > div.hpanel > iframe')
        ))
        form_url = form.get_attribute('src')
        self.driver.get(form_url)
        nom = spider.wait_css("input#form-2p-name")
        nom.send_keys('X')
        prenom = spider.wait_css("input#form-2p-firstname")
        prenom.send_keys('Y')
        birth = spider.wait_css("input#form-2p-birthday")
        for i in range(1950, 1981):
            print('Année en cours : %s' % i)
            birth.send_keys('01/01/%s' % i)
            buttonTwo = spider.wait_css("input#client_input")
            buttonTwo.click()
            '''founder = spider.wait_css("label.Switch-Size")
            for j in range(0,2):
                if j == 0:
                    pass
                else:
                    founder.click()'''
            sectors = spider.wait_all_xpath("//select[@id='form-2p-sector']//option[@value!=0]")
            for k in sectors:
                k.click()
                print('Secteur actuel : %s' % k.text)
                works = spider.wait_all_xpath("//select[@id='form-2p-work']//option[@value!=0]")
                for l in works:
                    l.click()
                    print('Travail actuel : %s' % l.text)
                    status = spider.wait_all_xpath("//select[@id='form-2p-status']//option[@value!=0]")
                    for m in status:
                        m.click()
                        print('Statut actuel : %s' % m.text)
                        regimes = spider.wait_all_xpath("//select[@id='form-2p-regime']//option[@value!=0]")
                        for n in regimes:
                            n.click()
                            print('Régime actuel : %s' % n.text)
                            buttonThree = spider.wait_css("button#etape_suivante")
                            buttonThree.click()
                            garanties = spider.wait_all_xpath("//select[@id='form-moteur-garantie']//option[@value!=0]")
                            for o in garanties:
                                o.click()
                                print('Garantie : %s' % o.text)
                                buttonFour = spider.wait_xpath("//input[@value='Valider']")
                                buttonFour.click()
                                time.sleep(2)
                                for p in range(0, 3):
                                    self.driver.execute_script(
                                        "document.querySelectorAll\
                                        ('span.glyphicon.glyphicon-triangle-bottom.open-close')[%s].click():" % p)
                                    time.sleep(1)
                                for q in range(0, 10):
                                    try:
                                        spider.scroll_to_element("input#incapacite-%s-1" % q)
                                        spider.click_js("input#incapacite-%s-1" % q)
                                        spider.scroll_to_element("input#tranquilite-%s-1" % q)
                                        spider.click_js("input#tranquilite-%s-1" % q)
                                        spider.scroll_to_element("input#deces_acc-%s-1" % q)
                                        spider.click_js("input#deces_acc-%s-1" % q)
                                        franchiseButton = spider.wait_xpath(
                                            "//select[@id='franchise-%s-1']/option[@value=18]" % q)
                                        franchiseButton.click()
                                        invaliditeButton = spider.wait_xpath(
                                            "//select[@id='invalidite-%s-1']/option[@value=3]" % q)
                                        invaliditeButton.click()
                                        renteduButton = spider.wait_xpath(
                                            "//select[@id='rente_education-%s-1']/option[@value=11]" % q)
                                        renteduButton.click()
                                    except WebDriverException:
                                        pass

                                for r in [5, 10, 15, 20]:
                                    for q in range(0,10):
                                        try:
                                            tcvButton = spider.wait_xpath(
                                                "//select[@id='taux_comm_courtier-%s-1']/option[@value=%s]" % (q, r)
                                            )
                                            tcvButton.click()
                                        except WebDriverException:
                                            pass


spider = SeleniumOiko()
spider.extract()
