from bs4 import BeautifulSoup
import os
from scrapy import Selector
import codecs
import json
import csv


class LeboncoinSpider:

    def __init__(self):
        self.path = '/Users/sashabouloudnine/Desktop/leboncoin_piscine'
        self.a = []
        self.count = 1

    def extraction_details(self):

        with codecs.open('gites_swimmy_11052018.csv', 'w') as csvfile:

            fieldnames = ['ID',
                          'Capacité',
                          'Piscine',
                          'Surface',
                          'Prix',
                          'Monnaie',
                          'Date',
                          'Localisation',
                          'Prix/m2',
                          'Titre',
                          'URL',
                          'Services'
                          ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="$")
            writer.writeheader()

            for i in os.listdir(self.path):

                if 'phone' in i:
                    pass

                else:

                    with open(self.path+"/"+i, "r") as f:

                        try:
                            a = json.load(f)

                            try:
                                id = a['id'].replace('\n', '')
                            except(KeyError, AttributeError):
                                id = ''
                                pass

                            try:
                                capacity = a['Capacité'].replace('\n', '')
                            except(KeyError, AttributeError):
                                capacity = ''
                                pass

                            try:
                                rooms = a['Nombre de chambres'].replace('\n', '')
                            except(KeyError, AttributeError):
                                rooms = ''
                                pass

                            try:
                                pool = a['Piscine'].replace('\n', '')
                            except(KeyError, AttributeError):
                                pool = ''
                                pass

                            try:
                                area = a['area'].replace('\n', '')
                            except(KeyError, AttributeError):
                                area = ''
                                pass

                            try:
                                cost = a['cost']
                            except(KeyError, AttributeError):
                                cost = ''
                                pass

                            try:
                                currency = a['currency'].replace('\n', '')
                            except(KeyError, AttributeError):
                                currency = ''
                                pass

                            try:
                                date = a['date'].replace('\n', '')
                            except(KeyError, AttributeError):
                                date = ''
                                pass

                            '''try:
                                description = a['description'].replace('\n', '')
                            except(KeyError, AttributeError):
                                description = ''
                                pass'''

                            try:
                                location = a['location'].replace('\n', '')
                            except(KeyError, AttributeError):
                                location = ''
                                pass

                            try:
                                price_per_meter = a['price_per_meter'].replace('\n', '')
                            except(KeyError, AttributeError):
                                price_per_meter = ''
                                pass

                            try:
                                title = a['title'].replace('\n', '')
                            except(KeyError, AttributeError):
                                title = ''
                                pass

                            try:
                                url = a['url'].replace('\n', '')
                            except(KeyError, AttributeError):
                                url = ''
                                pass

                            try:
                                utilities = a['utilities'].replace('\n', '')
                            except(KeyError, AttributeError):
                                utilities = ''
                                pass

                            writer.writerow({
                              'ID': id,
                              'Capacité': capacity,
                              'Piscine': pool,
                              'Surface': area,
                              'Prix': cost,
                              'Monnaie': currency,
                              'Date': date,
                              'Localisation': location,
                              'Prix/m2': price_per_meter,
                              'Titre': title,
                              'URL': url,
                              'Services': utilities
                            })

                            print("-- SUCCESS : %s %s --" % (i, self.count))
                            self.count += 1

                        except json.JSONDecodeError:
                            self.a.append(i)
                            print("-- FAILURE ")

    def extraction_phone(self):

        with codecs.open('gites_swimmy_11052018_phone.csv', 'w') as csvfile:

            fieldnames = ['ID',
                          'Téléphone'
                          ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="$")
            writer.writeheader()

            for i in os.listdir(self.path):

                if 'phone' in i:
                    with open(self.path + "/" + i, "r") as f:

                        a = json.load(f)

                        try:
                            id = a['id']
                        except KeyError:
                            id = ''
                            pass

                        try:
                            phone = a['phone']
                        except KeyError:
                            phone = ''
                            pass

                        writer.writerow({
                            'ID': id,
                            'Téléphone': phone
                        })

                        print("-- SUCCESS : %s %s --" % (i, self.count))
                        self.count += 1

                else:
                    pass


spider = LeboncoinSpider()
spider.extraction_details()
spider.extraction_phone()
