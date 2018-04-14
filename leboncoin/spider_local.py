from bs4 import BeautifulSoup
import os
import re
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import re
import codecs
import urllib
import json
import csv

# counter
count = 0

class spider:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count = self.count + 1

    def extraction(self):
        path = '/Users/sashabouloudnine/Desktop/aefcci'

        with codecs.open('aefcci.csv', 'w') as csvfile:
            fieldnames = ['Titre',
                          'Prix',
                          'Date',
                          'Honoraires',
                          'Type de bien',
                          'Reference',
                          'Piece',
                          'GES',
                          "Classe d'energie",
                          'Description',
                          'Ville',
                          'CP',
                          'Latitude',
                          'Longitude',
                          'Nom du representant',
                          'Adresse',
                          'SIRET',
                          'SIREN',
                          'Telephone',
                          'Prix au m2',
                          'Photo 1',
                          'Photo 2',
                          'Photo 3',
                          'Photo 4',
                          'Photo 5',
                          'Photo 6',
                          'Photo 7',
                          'Photo 8',
                          'Photo 9',
                          'Photo 10'
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
                        Titre = sel.xpath("//h1[@class='_1KQme']/text()").extract()[0]
                        Titre = Titre.encode('utf-8').replace('\xc3\xa8','e').replace('\xc2\xb2','2').replace('\n                   ','').replace('\n                  ', '')
                    except IndexError:
                        Titre = ''
                        pass

                    try:
                        Prix = sel.xpath("//div[@class='eVLNz']//div[@class='_386c2']//span[@class='_1F5u3']/text()").extract()[1]
                        Prix = Prix.encode('utf-8').replace('\n','').replace(' ','')
                    except IndexError:
                        Prix = ''
                        pass

                    try:
                        Date = sel.xpath("//div[@class='_3Pad-']/text()").extract()[0]
                        Date = Date.encode('utf-8').replace('\n                  ','').replace('\n                 ','').replace('\xc3\xa0','a')
                    except IndexError:
                        Date = ''
                        pass

                    try:
                        typebien = sel.xpath("//div[contains(text(),'Type de bien')]/following::div[1]/text()").extract()[0]
                        typebien = typebien.encode('utf-8').replace('\n                    ','').replace('\n                   ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        typebien = ''
                        pass

                    try:
                        Pieces = sel.xpath(u"//div[contains(text(),'Pi\xe8ces')]/following::div[1]/text()").extract()[0]
                        Pieces = Pieces.encode('utf-8').replace('\n                    ','').replace('\n                   ','')
                    except IndexError:
                        Pieces = ''
                        pass

                    try:
                        Honoraires = sel.xpath("//div[contains(text(),'Honoraires')]/following::div[1]/text()").extract()[0]
                        Honoraires = Honoraires.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        Honoraires = ''
                        pass

                    try:
                        Surface = sel.xpath("//div[contains(text(),'Surface')]/following::div[1]/text()").extract()[0]
                        Surface = Surface.encode('utf-8').replace('\n                    ','').replace('\n                   ','').replace('\xc2\xb2','2')
                    except IndexError:
                        Surface = ''
                        pass

                    try:
                        GES = sel.xpath("//span[contains(text(),'GES')]/following::div[1]//div[contains(@class, '_1sd0z')]/text()").extract()[0]
                        GES = GES.encode('utf-8').replace('\n                      ','').replace('\n                     ','')
                    except IndexError:
                        GES = ''
                        pass

                    try:
                        classeEn = sel.xpath(u"//span[contains(text(),'Classe \xe9nergie')]/following::div[1]//div[contains(@class, '_1sd0z')]/text()").extract()[0]
                        classeEn = classeEn.encode('utf-8').replace('\n                      ','').replace('\n                     ','')
                    except IndexError:
                        classeEn = ''
                        pass

                    try:
                        Description = sel.xpath("//div[@data-qa-id='adview_description_container']/div/span/text()").extract()
                        Description = ''.join(Description).encode('utf-8').replace('\n                  ', '').replace('\xc2\xb2','2').replace('\xc3\xa9','e')\
                                            .replace('\xc3\xa8','e').replace('\xe2\x82\xac', 'euros').replace('\xc3\xa0', 'a').replace('\xc2\xb0','o')
                    except IndexError:
                        Description = ''
                        pass

                    try:
                        Ville = sel.xpath("//div[@data-qa-id='adview_location_informations']/span/text()").extract()[1]
                        Ville = Ville.encode('utf-8').replace('\n                    ','').replace('\n                    ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        Ville = ''
                        pass

                    try:
                        CP = sel.xpath("//div[@data-qa-id='adview_location_informations']/span/text()").extract()[-2]
                        CP = CP.encode('utf-8').replace('\n                    ','').replace('\n                    ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        CP = ''
                        pass

                    try:
                        Latitude = sel.xpath("//script[contains(text(),'window.FLUX_STATE =')]").extract()
                        codeNAF = codeNAF.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        codeNAF = ''
                        pass

                    try:
                        libelleNAF = sel.xpath("//dt[contains(text(),' code NAF 2008')]/following::dd[1]/text()").extract()[0]
                        libelleNAF = libelleNAF.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        libelleNAF = ''
                        pass

                    try:
                        clair = sel.xpath("//dt[contains(text(),' en clair')]/following::dd[1]/text()").extract()[0]
                        clair = clair.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        clair = ''
                        pass

                    try:
                        SIREN = sel.xpath("//dt[contains(text(),'SIREN')]/following::dd[1]/text()").extract()[0]
                        SIREN = SIREN.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        SIREN = ''
                        pass

                    try:
                        rsociale = sel.xpath("//dt[contains(text(),'Raison sociale')]/following::dd[1]/text()").extract()[0]
                        rsociale = rsociale.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        rsociale = ''
                        pass

                    try:
                        denomination = sel.xpath("//dt[contains(text(),'nomination')]/following::dd[1]/text()").extract()[0]
                        denomination = denomination.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        denomination = ''
                        pass

                    try:
                        fj = sel.xpath("//dt[contains(text(),'Forme juridique')]/following::dd[1]/text()").extract()[0]
                        fj = fj.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        fj = ''
                        pass

                    try:
                        respo = sel.xpath("//dt[contains(text(),'Responsable l')]/following::dd[1]/text()").extract()[0]
                        respo = respo.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        respo = ''
                        pass

                    try:
                        cci = sel.xpath("//p[@class='ficheCCI']/a/text()").extract()[0]
                        cci = cci.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        cci = ''
                        pass

                    try:
                        Mail = sel.xpath("//dt[contains(text(),'mail')]/following::dd[1]/a/text()").extract()[0]
                        Mail = Mail.encode('utf-8').replace('\n           ','').replace('\n          ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        Mail = ''
                        pass

                    try:
                        siteinternet = sel.xpath("//dt[contains(text(),'Site internet')]/following::dd[1]/a/text()").extract()[0]
                        siteinternet = siteinternet.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        siteinternet = ''
                        pass

                    try:
                        sigle = sel.xpath("//dt[contains(text(),'Sigle')]/following::dd[1]/text()").extract()[0]
                        sigle = sigle.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        sigle = ''
                        pass

                    try:
                        capitalso = sel.xpath("//dt[contains(text(),'Capital social')]/following::dd[1]/text()").extract()[0]
                        capitalso = capitalso.encode('utf-8').replace('\n          ','').replace('\n         ','').replace('\xc3\xa8','e').replace('\xc3\xa9','e')
                    except IndexError:
                        capitalso = ''
                        pass

                    writer.writerow({
                                      'SIRET' : SIRET,
                                      'Enseigne' : Enseigne,
                                      'Statut' : Statut,
                                      'Categorie' : Categorie,
                                      'Voie' : Voie,
                                      'CP' : codepostal,
                                      'Ville' : Ville,
                                      'Pays' : Pays,
                                      "Date de debut d'activite" : datedeb,
                                      'Code APET' : CodeAPET,
                                      'Libelle code APET' : libelleAPET,
                                      'Code NAF 2008' : codeNAF,
                                      'Libelle code NAF 2008' : libelleNAF,
                                      'Activite en clair': clair,
                                      'SIREN': SIREN,
                                      'Raison sociale': rsociale,
                                      'Denomination': denomination,
                                      "Forme juridique": fj,
                                      'Responsable legal': respo,
                                      "Chambre de commerce et d'Industrie": cci,
                                      'Telephone': Telephone,
                                      'Mail' : Mail,
                                      'Site internet' : siteinternet,
                                      'Capital social' : capitalso,
                                      'Sigle' : sigle
                    })

                    print("-- SUCCESS : %s %s --" % (filename, self.count))
                    spider.increment()

spider = spider()
spider.extraction()