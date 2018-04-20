from bs4 import BeautifulSoup
import os
import re
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import re
import codecs
import urllib
import csv

class spider:

    def __init__(self):
        self.directory_name = "122016"
        self.count = 0
        self.path = '/Users/sashabouloudnine/PycharmProjects/scraping/sandbox/inpi/main_page_requests/' + self.directory_name


    def increment(self):
        self.count = self.count + 1

    def extraction(self):

        with codecs.open(self.directory_name + '.csv', 'w') as csvfile:
            fieldnames = ['marque',
                          'classification',
                          'numero',
                          'date',
                          'logo_name',
                          'deposant',
                          'deposant_nom',
                          'deposant_adress',
                          'deposant_ville',
                          'deposant_code_postal',
                          'deposant_pays',
                          'longueur_deposant',
                          'mandataire',
                          'mandataire_nom',
                          'mandataire_adress',
                          'mandataire_ville',
                          'mandataire_code_postal',
                          'mandataire_pays',
                          'longueur_mandataire'
                          ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="$")
            writer.writeheader()

            for filename in os.listdir(self.path):

                with open(self.path+"/"+filename, "r") as html_page:
                    soup = BeautifulSoup(html_page,
                                         features='html.parser',
                                         from_encoding='utf-8'
                                         )
                    sel = Selector(text=soup.prettify())

                    try:
                        marque = sel.xpath('//div[@class="blanc"]/div/p[contains(strong, "Marque")]/text()').extract()[1]
                        marque = marque.encode('utf-8').replace('\xc2\xa0','').\
                            replace('\n             :','').replace('\n            ','')
                    except IndexError:
                        marque = ''
                        pass

                    try:
                        classification = sel.xpath(
                        '//div[@class="blanc"]/div/p[contains(strong, "Classification de Nice")]/text()').extract()[1]
                        classification = classification.encode('utf-8').replace('\xc2\xa0','').\
                            replace('\n             :','').replace('\n            ','')
                    except(IndexError):
                        classification = ''
                        pass

                    try:
                        numero = sel.xpath('//div[@class="blanc"]/div/p[contains(strong, "Num")]/text()').extract()[1]
                        numero = numero.encode('utf-8').replace('\xc2\xa0','').\
                            replace('\n             :','').replace('\n            ','')
                    except(IndexError):
                        numero = ''
                        pass

                    try:
                        date = sel.xpath('//div[@class="blanc"]/div/p[contains(strong, "Date de")]/text()').extract()[1]
                        date = date.encode('utf-8').replace('\xc2\xa0','').\
                            replace('\n             :','').replace('\n            ','')
                    except(IndexError):
                        date = ''
                        pass

                    try:
                        deposant = sel.xpath('//div[@class="blanc"]/div/p[contains(strong, "posant")]/text()').extract()[1]
                        deposant = deposant.encode('utf-8').replace('\xc2\xa0','').\
                            replace('\n             :','').replace('\n            ','')
                        deposant = deposant.split(',')
                        longueur_deposant = len(deposant)
                        if longueur_deposant == 5:
                            deposant_nom = deposant[0]
                            deposant_adress = deposant[1]
                            deposant_code_postal = deposant[2]
                            deposant_ville = deposant[3]
                            deposant_pays = deposant[4]
                            deposant = ''

                        elif longueur_deposant == 6:
                            deposant_nom = str(deposant[0]) + ',' + str(deposant[1])
                            deposant_adress = deposant[2]
                            deposant_code_postal = deposant[3]
                            deposant_ville = deposant[4]
                            deposant_pays = deposant[5]
                            deposant = ''

                        elif longueur_deposant == 7:
                            deposant_nom = str(deposant[0]) + ',' + str(deposant[1])
                            deposant_adress = str(deposant[2]) + ',' + str(deposant[3])
                            deposant_code_postal = deposant[-3]
                            deposant_ville = deposant[-2]
                            deposant_pays = deposant[-1]
                            deposant = ''

                        elif longueur_deposant >= 8:
                            deposant_nom = str(deposant[0]) + ',' + str(deposant[1])
                            deposant.pop(0)
                            deposant.pop(0)
                            deposant_pays = deposant[-1]
                            deposant.pop(-1)
                            deposant_ville = deposant[-1]
                            deposant.pop(-1)
                            deposant_code_postal = deposant[-1]
                            deposant.pop(-1)
                            deposant_adress = ''
                            for i in reversed(range(len(deposant))):
                                deposant_adress += str(deposant[i])
                                deposant = ''

                        else:
                            deposant_nom = ''
                            deposant_adress = ''
                            deposant_code_postal = ''
                            deposant_ville = ''
                            deposant_pays = ''

                    except(IndexError):
                        deposant = ''
                        deposant_pays = ''
                        deposant_ville = ''
                        deposant_code_postal = ''
                        deposant_nom = ''
                        deposant_adress = ''
                        longueur_deposant = ''
                        pass

                    try:
                        mandataire = sel.xpath('//div[@class="blanc"]/div/p[contains(strong, "Mandataire")]/text()').extract()[1]
                        mandataire = mandataire.encode('utf-8').replace('\xc2\xa0','').\
                            replace('\n             :','').replace('\n            ','')
                        mandataire = mandataire.split(',')
                        longueur_mandataire = len(mandataire)
                        if longueur_mandataire == 5:
                            mandataire_nom = mandataire[0]
                            mandataire_adress = mandataire[1]
                            mandataire_code_postal = mandataire[2]
                            mandataire_ville = mandataire[3]
                            mandataire_pays = mandataire[4]
                            mandataire = ''

                        elif longueur_mandataire == 6:
                            mandataire_nom = str(mandataire[0]) + ',' + str(mandataire[1])
                            mandataire_adress = mandataire[2]
                            mandataire_code_postal = mandataire[3]
                            mandataire_ville = mandataire[4]
                            mandataire_pays = mandataire[5]
                            mandataire = ''

                        elif longueur_mandataire == 7:
                            mandataire_nom = str(mandataire[0]) + ',' + str(mandataire[1])
                            mandataire_adress = str(mandataire[2]) + ',' + str(mandataire[3])
                            mandataire_code_postal = mandataire[-3]
                            mandataire_ville = mandataire[-2]
                            mandataire_pays = mandataire[-1]
                            mandataire = ''

                        elif longueur_mandataire >= 8:
                            mandataire_nom = str(mandataire[0]) + ',' + str(mandataire[1])
                            mandataire.pop(0)
                            mandataire.pop(0)
                            mandataire_pays = mandataire[-1]
                            mandataire.pop(-1)
                            mandataire_ville = mandataire[-1]
                            mandataire.pop(-1)
                            mandataire_code_postal = mandataire[-1]
                            mandataire.pop(-1)
                            mandataire_adress = ''
                            for i in reversed(range(len(mandataire))):
                                mandataire_adress += str(mandataire[i])
                            mandataire = ''

                        else:
                            mandataire_nom = ''
                            mandataire_adress = ''
                            mandataire_code_postal = ''
                            mandataire_ville = ''
                            mandataire_pays = ''

                    except(IndexError):
                        mandataire = ''
                        mandataire_pays = ''
                        mandataire_ville = ''
                        mandataire_code_postal = ''
                        mandataire_nom = ''
                        mandataire_adress = ''
                        longueur_mandataire = ''
                        pass


                    logo_name = ('logo_%s' % self.count).encode('utf-8')

                    writer.writerow({'marque': marque,
                                     'classification': classification,
                                     'numero': numero,
                                     'date': date,
                                     'deposant' : deposant,
                                     'deposant_pays' : deposant_pays,
                                     'deposant_ville' : deposant_ville,
                                     'deposant_code_postal' : deposant_code_postal,
                                     'deposant_nom' : deposant_nom,
                                     'deposant_adress' : deposant_adress,
                                     'longueur_deposant' : longueur_deposant,
                                     'mandataire' : mandataire,
                                     'mandataire_pays' : mandataire_pays,
                                     'mandataire_ville' : mandataire_ville,
                                     'mandataire_code_postal' : mandataire_code_postal,
                                     'mandataire_nom' : mandataire_nom,
                                     'mandataire_adress' : mandataire_adress,
                                     'longueur_mandataire' : longueur_mandataire,
                                     'logo_name': logo_name})

                    print("-- SUCCESS %s --" % (self.count))
                    spider.increment()

spider = spider()
spider.extraction()

os.system('say "travail terminai"')