# python package
import csv
import time

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
        self.wait = WebDriverWait(self.driver, 20)
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

    def connect(self, url):
        self.driver.get(url)

        # pause
        time.sleep(5)

        identifiant = spider.wait_css("input#Login")
        password = spider.wait_css("input#Password")
        identifiant.send_keys("09051123")
        password.send_keys("cUMZg6AYZ478tt28")
        button_one = spider.wait_css("button.btn.btn-login.submit-button")
        button_one.click()
        print('Connecté à : %s' % url)

        form = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.content > div.hpanel > iframe')
        ))
        form_url = form.get_attribute('src')
        self.driver.get(form_url)

    def connect_back(self, url):
        self.driver.get(url)

        # pause
        time.sleep(5)

        form = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.content > div.hpanel > iframe')
        ))
        form_url = form.get_attribute('src')
        self.driver.get(form_url)

    def toggle(self):
        # Toggle pour toutes les sous-catégories
        toggle_incapacite = self.driver.find_element_by_xpath(
            "//div[@class='item active']/div[@id='accordion1-1']\
            /div[@class='panel panel-default']\
            /div[@class='panel-heading clearfix']\
            /h4[@class='panel-title l-panel-head title-work']\
            /span[text()='INCAPACITÉ DE TRAVAIL']\
            /ancestor::div[1]/div[@class='pull-right']\
            /span[@class='glyphicon glyphicon-triangle-bottom open-close']"
        )
        spider.click_js(toggle_incapacite)
        toggle_invalidite = self.driver.find_element_by_xpath(
            "//div[@class='item active']/div[@id='accordion1-1']\
            /div[@class='panel panel-default']\
            /div[@class='panel-heading clearfix']\
            /h4[@class='panel-title l-panel-head title-invalid']\
            /span[text()='INVALIDITÉ']\
            /ancestor::div[1]/div[@class='pull-right']\
            /span[@class='glyphicon glyphicon-triangle-bottom open-close']"
        )
        spider.click_js(toggle_invalidite)
        toggle_deces = self.driver.find_element_by_xpath(
            "//div[@class='item active']/div[@id='accordion1-1']\
            /div[@class='panel panel-default']\
            /div[@class='panel-heading clearfix']\
            /h4[@class='panel-title l-panel-head title-deces']\
            /span[text()='DÉCÈS PAR ACCIDENT']\
            /ancestor::div[1]/div[@class='pull-right material-switch']\
            /span[@class='glyphicon glyphicon-triangle-bottom open-close']"
        )
        spider.click_js(toggle_deces)
        toggle_education = self.driver.find_element_by_xpath(
            "//div[@class='item active']/div[@id='accordion1-1']\
            /div[@class='panel panel-default']\
            /div[@class='panel-heading clearfix']\
            /h4[@class='panel-title l-panel-head title-rente']\
            /span[text()='RENTES']\
            /ancestor::div[1]/div[@class='pull-right material-switch']\
            /span[@class='glyphicon glyphicon-triangle-bottom open-close']"
        )
        spider.click_js(toggle_education)

    def organize_page(self, num_page, id_value):
        title_active_page = self.driver.find_element_by_xpath(
            "//div[@class='item active']/\
            div[@id='accordion1-1']/div[@class='panel panel-default']/div[@class='panel-heading clearfix']\
            /h3[@class='offre_title majuscule']/span[@style='text-transform: none;']"
        ).text
        while title_active_page != '%s' % num_page:
            next_page_button = spider.wait_xpath("//a[@data-slide='next']")
            spider.click_js(next_page_button)
            time.sleep(2)
            title_active_page = spider.wait_xpath(
                "//div[@class='item active']/\
                div[@id='accordion1-1']/div[@class='panel panel-default']/div[@class='panel-heading clearfix']\
                /h3[@class='offre_title majuscule']/span[@style='text-transform: none;']"
            ).text

        input_incapacite = self.driver.find_element_by_xpath(
            "//input[@id='incapacite-%s-1']" % id_value
        )
        spider.scroll_to_element(input_incapacite)
        if input_incapacite.get_attribute('aria-expanded') == 'true':
            spider.click_js(input_incapacite)
        else:
            pass

        input_tranquillite = self.driver.find_element_by_xpath(
            "//input[@id='tranquillite-%s-1']" % id_value
        )
        spider.scroll_to_element(input_tranquillite)
        if input_tranquillite.get_attribute('aria-expanded') == 'true':
            spider.click_js(input_tranquillite)
        else:
            pass

        input_deces_acc = self.driver.find_element_by_xpath(
            "//input[@id='deces_acc-%s-1']" % id_value
        )
        spider.scroll_to_element(input_deces_acc)
        if input_deces_acc.get_attribute('aria-expanded') == 'true':
            spider.click_js(input_deces_acc)
        else:
            pass

        franchise_button = self.driver.find_element_by_xpath(
            "//select[@id='franchise-%s-1']/option[@value=18]" % id_value
        )
        spider.scroll_to_element(franchise_button)
        franchise_button.click()
        invalidite_button = self.driver.find_element_by_xpath(
            "//select[@id='invalidite-%s-1']/option[@value=3]" % id_value
        )
        spider.scroll_to_element(invalidite_button)
        invalidite_button.click()
        rente_edu_button = self.driver.find_element_by_xpath(
            "//select[@id='rente_education-%s-1']/option[@value=11]" % id_value
        )
        spider.scroll_to_element(rente_edu_button)
        rente_edu_button.click()

    def exside(self, a, b, c, d, e, f, u):
        with open(path + "/" + "oiko_extract_18022018_1.csv", "a") as mycsv:
            fieldnames = ["Date de naissance",
                          "Createur d'entreprise",
                          "Secteur d'activité",
                          "Profession",
                          "Statut",
                          "Régime",
                          "Garantie",
                          "TPRO",
                          "TCV",
                          "Taux en % de la base",
                          "Tarif mensuel",
                          "Dont déductible Madelin",
                          "CMV"]
            writer = csv.DictWriter(mycsv, fieldnames=fieldnames, delimiter='$')
            writer.writeheader()

            # Remplir le formulaire
            nom = spider.wait_css("input#form-2p-name")
            nom.send_keys('X')
            prenom = spider.wait_css("input#form-2p-firstname")
            prenom.send_keys('Y')
            date = spider.wait_css("input#form-2p-birthday")
            date.send_keys('01/01/%s' % a)
            button_two = spider.wait_css("input#client_input")
            button_two.click()

            # pause
            time.sleep(5)

            founder = self.driver.find_element_by_xpath(
                "//input[@id='form-2p-thisyear']"
            )
            if float(u) == 1:
                spider.click_js(founder)
            else:
                pass
            sector = self.driver.find_element_by_xpath('//select[@id="form-2p-sector"]/option[text()="%s"]' % c)
            sector.click()
            work = spider.wait_xpath('//select[@id="form-2p-work"]/option[text()="%s"]' % d)
            work.click()
            status = spider.wait_xpath('//select[@id="form-2p-status"]/option[text()="%s"]' % e)
            status.click()
            regime = spider.wait_xpath('//select[@id="form-2p-regime"]/option[text()="%s"]' % f)
            regime.click()
            button_three = spider.wait_css("button#etape_suivante")
            button_three.click()

            # pause
            time.sleep(5)

            garantie_trigger = spider.wait_xpath("//select[@id='form-moteur-garantie']/option[@value=0.5]")
            garantie_trigger.click()
            button_four = spider.wait_xpath("//input[@value='Valider']")
            button_four.click()

            # pause
            time.sleep(5)

            # Toggle pour toutes les sous-catégories
            spider.toggle()

            # Paramétrer la page de collecte
            spider.organize_page(3, 8)

            # Collecter les données de la page
            num_page = 8
            id_page = 3
            garantie_list = self.driver.find_elements_by_xpath("//select[@id='form-moteur-garantie']/option")
            for i in garantie_list:
                if float(i.get_attribute('value')) % 0.5 == 0:
                    i.click()
                    g_1 = i.text
                    for tcv_1 in [5, 10, 15, 20]:
                        tcv_button = self.driver.find_element_by_xpath(
                            "//select[contains(@id, 'taux_comm_courtier-%s-1')]/option[@value=%s]" %
                            (num_page, tcv_1)
                        )
                        spider.scroll_to_element(tcv_button)
                        tcv_button.click()

                        # Récupérer les données

                        tpro_value_1 = id_page

                        taux_pourcent_base_1 = spider.wait_xpath(
                            "//span[@id='taux-%s-1']" % num_page
                        )
                        taux_pourcent_base_1 = taux_pourcent_base_1.text
                        tarif_mensuel_1 = spider.wait_xpath(
                            "//span[@id='TTC-%s-1']" % num_page
                        )
                        tarif_mensuel_1 = tarif_mensuel_1.text
                        deduc_madelin_1 = spider.wait_xpath(
                            "//span[@id='dont_madelin-%s-1']" % num_page
                        )
                        deduc_madelin_1 = deduc_madelin_1.text
                        cmv_1 = spider.wait_xpath(
                            "//span[@id='total_comm-%s-1']" % num_page
                        )
                        cmv_1 = cmv_1.text

                        # Ecrire les valeurs dans le .csv
                        writer.writerow({
                            "Date de naissance": a,
                            "Createur d'entreprise": b,
                            "Secteur d'activité": c,
                            "Profession": d,
                            "Statut": e,
                            "Régime": f,
                            "Garantie": g_1,
                            "TPRO": tpro_value_1,
                            "TCV": tcv_1,
                            "Taux en % de la base": taux_pourcent_base_1,
                            "Tarif mensuel": tarif_mensuel_1,
                            "Dont déductible Madelin": deduc_madelin_1,
                            "CMV": cmv_1
                        })


            # Paramétrer la page de collecte
            time.sleep(5)
            spider.organize_page(4, 9)

            # Collecter les données de la page
            num_page = 9
            id_page = 4
            garantie_list = self.driver.find_elements_by_xpath("//select[@id='form-moteur-garantie']/option[@value!=0]")
            for i in garantie_list:
                if float(i.get_attribute('value')) % 0.5 == 0:
                    i.click()
                    g_2 = i.text
                    for tcv_2 in [5, 10, 15, 20]:
                        tcv_button = self.driver.find_element_by_xpath(
                            "//select[@id='taux_comm_courtier-%s-1']/option[@value=%s]" % (
                                num_page, tcv_2)
                        )
                        spider.scroll_to_element(tcv_button)
                        tcv_button.click()

                        # Récupérer les données

                        tpro_value_2 = id_page

                        taux_pourcent_base_2 = spider.wait_xpath(
                            "//span[@id='taux-%s-1']" % num_page
                        )
                        taux_pourcent_base_2 = taux_pourcent_base_2.text
                        tarif_mensuel_2 = spider.wait_xpath(
                            "//span[@id='TTC-%s-1']" % num_page
                        )
                        tarif_mensuel_2 = tarif_mensuel_2.text
                        deduc_madelin_2 = spider.wait_xpath(
                            "//span[@id='dont_madelin-%s-1']" % num_page
                        )
                        deduc_madelin_2 = deduc_madelin_2.text
                        cmv_2 = spider.wait_xpath(
                            "//span[@id='total_comm-%s-1']" % num_page
                        )
                        cmv_2 = cmv_2.text

                        # Ecrire les valeurs dans le .csv
                        writer.writerow({
                            "Date de naissance": a,
                            "Createur d'entreprise": b,
                            "Secteur d'activité": c,
                            "Profession": d,
                            "Statut": e,
                            "Régime": f,
                            "Garantie": g_2,
                            "TPRO": tpro_value_2,
                            "TCV": tcv_2,
                            "Taux en % de la base": taux_pourcent_base_2,
                            "Tarif mensuel": tarif_mensuel_2,
                            "Dont déductible Madelin": deduc_madelin_2,
                            "CMV": cmv_2
                        })

            spider.connect_back("https://extranet.axelliance-solution.com/Tarifer/Tarificateur/TimeProTNSPrev")


spider = SeleniumOiko()

path = "/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/oiko"
with open(path + "/" + 'categories2.csv', 'r') as o:
    reader = csv.DictReader(o, fieldnames=["Date de naissance", "Createur d'entreprise","Activation du bouton",
                                           "Secteur d'activité", "Profession", "Statut", "Régime"], delimiter='$')
    # Se connecter à Prévoyance
    url_prevoyance = "https://extranet.axelliance-solution.com/Tarifer/Tarificateur/TimeProTNSPrev"
    spider.connect(url_prevoyance)

    for row in reader:
        a = row['Date de naissance']
        b = row["Createur d'entreprise"]
        c = row["Secteur d'activité"]
        d = row["Profession"]
        e = row["Statut"]
        f = row["Régime"]
        u = row["Activation du bouton"]

        if a == "Date de naissance":
            pass
        else:
            print(a, b, c, d, e, f, u)
            spider.exside(a, b, c, d, e, f, u)

'''
with open(path+'/'+'categories2.csv', w) as o:
    fieldnames = ["Date de naissance",
                  "Createur d'entreprise",
                  "Secteur d'activité",
                  "Profession",
                  "Statut",
                  "Régime"]
    writer = csv.DictWriter(mycsv, fieldnames=fieldnames, delimiter='$')
    writer.writeheader()
    for i in [1988, 1978, 1971, 1961]:
        for j in [0,1]:
            a = driver.find_elements_by_xpath("//select[@id='form-2p-sector']/option[@value!=0]")
            for k in a:
                k = k.text
                b = driver.find_elements_by_xpath("//select[@id='form-2p-work']/option[@value!=0]")
                for l in b:
                    l = l.text
                    c = driver.find_element_by_xpath("//select[@id='form-2p-status']/option[@value!=0 and text()!='Conjoint Collaborateur']")
                    for m in c:
                        m = m.text
                        d = c = driver.find_element_by_xpath("//select[@id='form-2p-regime']/option[@value!=0]")
                        for n in d:
                            n = n.text
                            writer.writerow({
                                "Date de naissance": i,
                                "Createur d'entreprise": j,
                                "Secteur d'activité": k,
                                "Profession": l,
                                "Statut": m,
                                "Régime": n
                            })

'''

