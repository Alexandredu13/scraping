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

    def scroll_down(self, percentage):
        return self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*arguments[0]);", percentage)

    def click_js(self, element):
        return self.driver.execute_script("arguments[0].click();", element)

    def connect(self):
        self.driver.get(self.url1)
        identifiant = spider.wait_css("input#Login")
        password = spider.wait_css("input#Password")
        # pause
        time.sleep(5)
        identifiant.send_keys("09051123")
        password.send_keys("cUMZg6AYZ478tt28")
        buttonOne = spider.wait_css("button.btn.btn-login.submit-button")
        buttonOne.click()
        print('Connecté à : %s' % self.url2)

    def extract(self):
        SeleniumOiko.connect(self)
        # pause
        time.sleep(5)
        sante_bloc = spider.wait_xpath("//h4[text()='Santé et Prévoyance TNS']")
        sante_bloc.click()
        # pause
        time.sleep(5)
        print('Connecté à : %s' % self.url3)
        urlPrevoyance = spider.wait_css("a#url-tarificateur-42")
        #urlSante = SeleniumOiko.wait_css("a#url-tarificateur-43")
        urlPrevoyance.click()
        # pause
        time.sleep(5)
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
                                # pause
                                time.sleep(5)
                                spider.scroll_down(0.3)
                                toggle_incapacite = self.driver.find_element_by_xpath(
                                    "//span[text()='INCAPACITÉ DE TRAVAIL']\
                                    /ancestor::div[1]/div[@class='pull-right']\
                                    /span[@class='glyphicon glyphicon-triangle-bottom open-close']")
                                toggle_invalidite = self.driver.find_element_by_xpath(
                                    "//span[text()='INVALIDITÉ']/ancestor::div[1]\
                                    /div[@class='pull-right']\
                                    /span[@class='glyphicon glyphicon-triangle-bottom open-close']")
                                toggle_deces = self.driver.find_element_by_xpath(
                                    "//span[text()='DÉCÈS PAR ACCIDENT']/ancestor::div[1]\
                                    /div[@class='pull-right material-switch']\
                                    /span[@class='glyphicon glyphicon-triangle-bottom open-close']")
                                toggle_education = self.driver.find_element_by_xpath(
                                    "//span[text()='RENTES']/ancestor::div[1]\
                                    /div[@class='pull-right material-switch']\
                                    /span[@class='glyphicon glyphicon-triangle-bottom open-close']"
                                )
                                table_toggle = []
                                table_toggle.append(toggle_incapacite)
                                table_toggle.append(toggle_invalidite)
                                table_toggle.append(toggle_deces)
                                table_toggle.append(toggle_education)
                                for i in table_toggle:
                                    spider.scroll_to_element(i)
                                    spider.click_js(i)
                                    time.sleep(1)
                                input_incapacite = self.driver.find_element_by_xpath("//input[@id='incapacite-7-1']")
                                input_tranquillite = self.driver.find_element_by_xpath("//input[@id='tranquillite-7-1']")
                                input_deces_acc = self.driver.find_element_by_xpath("//input[@id='deces_acc-7-1']")
                                franchise_button = self.driver.find_element_by_xpath("//select[@id='franchise-7-1']\
                                    /option[@value=18]")
                                invalidite_button = self.driver.find_element_by_xpath("//select[@id='invalidite-7-1']\
                                    /option[@value=3]")
                                rente_button = self.driver.find_element_by_xpath("//select[@id='rente_education-%s-1']\
                                    /option[@value=11]")
                                rente_edu_button = self.driver.find_element_by_xpath(
                                    "//select[@id='rente_education-7-1']/option[@value=11]"
                                )
                                spider.scroll_to_element(input_incapacite)
                                spider.click_js(input_incapacite)
                                spider.scroll_to_element(input_tranquillite)
                                spider.click_js(input_tranquillite)
                                spider.scroll_to_element(input_deces_acc)
                                spider.click_js(input_deces_acc)
                                spider.scroll_to_element(franchise_button)
                                spider.click_js(franchise_button)
                                spider.scroll_to_element(invalidite_button)
                                spider.click_js(invalidite_button)
                                spider.scroll_to_element(rente_button)
                                spider.click_js(rente_button)
                                spider.scroll_to_element(rente_edu_button)
                                spider.click_js(rente_edu_button)

                                for r in [5, 10, 15, 20]:
                                        try:
                                            tcv_button = spider.wait_xpath(
                                                "//select[@id='taux_comm_courtier-7-1']/option[@value=%s]" % r
                                            )
                                            spider.scroll_to_element(tcv_button)
                                            spider.click_js(tcv_button)
                                        except WebDriverException:
                                            pass


spider = SeleniumOiko()
spider.extract()
