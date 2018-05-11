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
from selenium.common.exceptions import NoSuchElementException


# fonction pause
def pause():
    time_break = random.randint(1, 2)
    return time.sleep(time_break)


# options
path_to_webdriver = "my_path"
options = webdriver.ChromeOptions()
options.add_argument("--kiosk")
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
driver = webdriver.Chrome("/Users/sashabouloudnine/Desktop/chromedriver", desired_capabilities=capa, chrome_options=options)
wait = WebDriverWait(driver, 30)
pause()

# url de depart
lequipe_url = "https://www.lequipe.fr/Football/Coupe-du-monde/Saison-2018/calendrier-resultats.html"

# aller sur lequipe
driver.get(lequipe_url)
images = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "img"))
            )

# scroller jusqu'en bas de page
scheight = .0
while scheight < 1.0:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*%s);" % scheight)
    scheight += .2
    pause()

# ouvrir csv
with codecs.open('lequipe_coupedumonde.csv', 'w') as csvfile:
    fieldnames = ['Date', 'Groupe', 'Ville', 'Nation 1', 'Nation 2', 'Heure', 'TV']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="$")
    writer.writeheader()

    # bloc d'éléments 1
    bloc1 = driver.find_elements_by_css_selector("section.mainDate")

    # boucle 1
    for i in bloc1:

        try:
            date = i.get_attribute('data-date')
        except NoSuchElementException:
            date = ''
            pass

        # bloc d'éléments 2
        bloc2 = i.find_elements_by_css_selector("table.ResultatGroupe.Cal_Ag > tbody > tr")

        # boucle 2
        for j in bloc2:

            # scroll doucement
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",
                j)

            # groupe
            try:
                group = j.find_element_by_css_selector("td.date > strong").text
            except NoSuchElementException:
                group = ''
                pass

            # ville
            try:
                city = j.find_element_by_css_selector("td.date > strong").text
                city = city.strip()
            except NoSuchElementException:
                city = ''
                pass

            # nation 1
            try:
                nationOne = j.find_element_by_css_selector("td.domicile.equipe1 > a").text
            except NoSuchElementException:
                try:
                    nationOne = j.find_element_by_css_selector("td.domicile.equipe1 > span").text
                except NoSuchElementException:
                    nationOne = ''
                    pass

            # nation 2
            try:
                nationTwo = j.find_element_by_css_selector("td.exterieur.rencontre2 > a").text
            except NoSuchElementException:
                try:
                    nationTwo = j.find_element_by_css_selector("td.exterieur.rencontre2 > span").text
                except NoSuchElementException:
                    nationTwo = ''
                    pass

            # heure de diffusion
            try:
                timeTv = j.find_element_by_css_selector("span.heurematch").text
            except NoSuchElementException:
                timeTv = ''
                pass

            # chaîne(s) télé
            try:
                tv = j.find_element_by_css_selector("td.diffuseur > span").text
            except NoSuchElementException:
                tv = ''
                pass

            # write csv
            writer.writerow({'Date': date, 'Groupe': group, 'Ville': city, 'Nation 1': nationOne,
                             'Nation 2': nationTwo, 'Heure': timeTv, 'TV': tv})

            print("-- SUCCESS : %s vs. %s --" % (nationOne, nationTwo))
            pause()

# fin
print("Bravo !")
driver.close()
