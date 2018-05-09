from bs4 import BeautifulSoup
import os
from scrapy import Selector
import codecs
import csv
import datetime

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class SpiderCenior:

    def __init__(self):
        self.count = 0
        self.today = str(datetime.date.today()).replace('-', '')

    def increment(self):
        self.count = self.count + 1

    def extraction(self):
        path = '/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/cenior/profiles/'

        with codecs.open('profiles_cenior_%s.csv' % self.today, 'w') as csvfile:
            fieldnames = ['Nom',
                          'Titre',
                          'Adresse',
                          'Code postal',
                          'Ville',
                          'Telephone',
                          'Mail',
                          'URL',
                          'Categorie'
                          ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="$")
            writer.writeheader()

            for filename in os.listdir(path):

                with open(path+"/"+filename, "r") as html_page:
                    soup = BeautifulSoup(html_page,
                                         features='html.parser',
                                         from_encoding='utf-8'
                                         )
                    sel = Selector(text=soup.prettify())

                    try:
                        largeTitle = sel.xpath("//span[@class='nom']/text()").extract()[0].strip()
                    except IndexError:
                        largeTitle = ''
                        pass

                    if largeTitle is not '':
                        name = largeTitle[:largeTitle.find(' -')].replace('-', '')
                        title = largeTitle[largeTitle.rfind('-'):].replace('- ', '').replace('-', '')
                    else:
                        name = ''
                        title = ''
                        pass

                    try:
                        adress = sel.xpath("//span[@class='adresse']/text()").extract()[0].strip()
                    except IndexError:
                        adress = ''

                    try:
                        largeAdress = sel.xpath("//span[@class='adresse']/text()").extract()[1].strip()
                        largeAdress = largeAdress.split()
                        cp = largeAdress[0]
                        ville = ' '.join(largeAdress[1:])
                    except IndexError:
                        cp = ''
                        ville = ''
                        pass

                    try:
                        phone = sel.xpath("//span[@class='telephone']/a/text()").extract()[0].strip()
                    except IndexError:
                        phone = ''
                        pass

                    try:
                        largeMail = sel.xpath("//span[@class='email']/a/text()").extract()
                        mail = largeMail[0].strip() + '@' + largeMail[1].strip()
                    except IndexError:
                        mail = ''
                        pass

                    try:
                        url = sel.xpath("//span[@class='url']/a/text()").extract()[0].strip()
                    except IndexError:
                        url = ''
                        pass

                    try:
                        category = sel.xpath("//h2[@class='intitule']/text()").extract()[0].strip()
                    except IndexError:
                        category = ''
                        pass

                    writer.writerow({
                                      'Nom': name,
                                      'Titre': title,
                                      'Adresse': adress,
                                      'Ville': ville,
                                      'Code postal': cp,
                                      'Telephone': phone,
                                      'Mail': mail,
                                      'URL': url,
                                      "Categorie": category
                    })

                    print("-- SUCCESS : %s %s --" % (self.count, filename))
                    SpiderCenior.increment(self)


a = SpiderCenior()
a.extraction()
