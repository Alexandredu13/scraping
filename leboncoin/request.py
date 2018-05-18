import requests
from bs4 import BeautifulSoup
from scrapy import Selector
import os
import csv
import json


class SpiderLeboncoin():

    def __init__(self):
        self.r = requests.session()
        self.sel = Selector
        self.count = 0

    def parse(self, a):
        soup = BeautifulSoup(a, features='html.parser')
        self.sel = Selector(text=soup.prettify())
        return self.sel

    def extract(self, i):
        print('Page : %s' % i)
        a = self.r.get("https://www.leboncoin.fr/_immobilier_/offres/?o=%s&location=Toulouse" % i)
        a = a.text
        SpiderLeboncoin.parse(self, a)
        annonces_url = self.sel.xpath("//section[@class='tabsContent block-white dontSwitch']/ul/li/a/@href").extract()
        for j in annonces_url:
            url = 'http://' + j.replace('//', '')
            j = j.replace('//', '').replace('/', '-')
            print(url)
            html_response = self.r.get(url).text
            with open('/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/leboncoin/pages/%s.htm' % j, "w") as f:
                f.write(html_response)

    def extract_local(self, path):
        with open(
                "/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/leboncoin/rabinovitch_sample_18052018.csv", 'w'
        ) as csv_file:
                fieldnames = ['Titre',
                              "Type d'annonce",
                              "Type de bien",
                              "Nombre de pièces",
                              'Surface',
                              'GES',
                              "Classe d'énergie",
                              "Prix",
                              "Ville",
                              "Code postal",
                              "Latitude",
                              "Longitude",
                              "Département",
                              "Région",
                              "Date",
                              "Meublé/Non meublé",
                              'URL',
                              "Description"
                              ]

                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter="$")
                writer.writeheader()

                for filename in os.listdir(path=path):
                    with open(path+"/"+filename, "r") as page_to_scrap:
                        SpiderLeboncoin.parse(self, page_to_scrap)

                        try:
                            a = self.sel.xpath(
                                "//script[contains(text(), 'window.FLUX_STATE')]/text()"
                                ).extract()[0].replace('\n   window.FLUX_STATE = ', '').replace('\n  ', '')
                            a = json.loads(a)

                            try:
                                title = a['adview']['subject']
                            except(IndexError, KeyError):
                                title = ''

                            try:
                                type_annonce = a['adview']['category_name']
                            except(IndexError, KeyError):
                                type_annonce = ''

                            type_bien = ''
                            rooms = ''
                            square = ''
                            ges = ''
                            energy_rate = ''
                            furnished = ''

                            try:
                                attributes = a['adview']['attributes']
                                for i in attributes:
                                    if i['key'] == 'real_estate_type':
                                        type_bien = i['value_label']
                                    if i['key'] == 'rooms':
                                        rooms = i['value_label']
                                    if i['key'] == 'square':
                                        square = i['value_label']
                                    if i['key'] == 'GES':
                                        ges = i['value_label']
                                    if i['key'] == 'energy_rate':
                                        energy_rate = i['value_label']
                                    if i['key'] == 'furnished':
                                        furnished = i['value_label']

                            except(IndexError, KeyError):
                                type_bien = ''
                                rooms = ''
                                square = ''
                                ges = ''
                                energy_rate = ''
                                furnished = ''

                            try:
                                description = a['adview']['body'].replace('\n', ' ')
                            except(IndexError, KeyError):
                                description = ''

                            try:
                                price = a['adview']['price'][0]
                            except(IndexError, KeyError):
                                price = ''

                            try:
                                city = a['adview']['location']['city']
                            except(IndexError, KeyError):
                                city = ''

                            try:
                                zipcode = a['adview']['location']['zipcode']
                            except(IndexError, KeyError):
                                zipcode = ''

                            try:
                                lat = a['adview']['location']['lat']
                            except(IndexError, KeyError):
                                lat = ''

                            try:
                                lng = a['adview']['location']['lng']
                            except(IndexError, KeyError):
                                lng = ''

                            try:
                                department_name = a['adview']['location']['department_name']
                            except(IndexError, KeyError):
                                department_name = ''

                            try:
                                region_name = a['adview']['location']['region_name']
                            except(IndexError, KeyError):
                                region_name = ''

                            try:
                                date = a['adview']['first_publication_date']
                            except(IndexError, KeyError):
                                date = ''

                            try:
                                url = a['adview']['url']
                            except(IndexError, KeyError):
                                url = ''

                            writer.writerow({
                              'Titre': title,
                              "Type d'annonce": type_annonce,
                              "Type de bien": type_bien,
                              "Nombre de pièces": rooms,
                              'Surface': square,
                              'GES': ges,
                              "Classe d'énergie": energy_rate,
                              "Prix": price,
                              "Ville": city,
                              "Code postal": zipcode,
                              "Latitude": lat,
                              "Longitude": lng,
                              "Département": department_name,
                              "Région": region_name,
                              "Date": date,
                              "Meublé/Non meublé": furnished,
                              'URL': url,
                              "Description": description
                            })

                            print("-- SUCCESS : %s %s --" % (filename, self.count))
                            self.count += 1

                        except(IndexError, KeyError):
                            pass


lbc_spider = SpiderLeboncoin()
lbc_spider.extract_local("/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/leboncoin/pages")