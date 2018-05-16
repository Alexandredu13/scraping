import threading
import pickle
import requests
from requests import exceptions
from requests import Request, Session
from random import randint
from bs4 import BeautifulSoup
import os
import re
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import re
import codecs
import urllib
import requests
import csv
from threading import Thread
import os
import time
from bs4 import BeautifulSoup
from scrapy import Selector


class inpi_request(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.s = requests.Session()
        self.count = 0
        self.error_table = []
        self.year = "2018"
        self.month = "04"
        self.total_days = 30
        self.starting_day = 1
        self.local_directory = self.month + self.year + "/"
        self.url_directory = "/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/inpi/main_page_requests/" + \
                             self.local_directory

    def increment(self):
        self.count = self.count + 1

    def run(self):
        for date in inpi_request.dates(self):
            while True:
                try:
                    print('spider-' + str(self.threadID) + ' : entering')
                    inpi_request.entry(self)
                    print('spider-' + str(self.threadID) + ' : in')
                    inpi_request.postman(self, self.threadID, date)
                    print('spider-' + str(self.threadID) + ' : done')
                    time.sleep(0.5)
                except(exceptions.ChunkedEncodingError, exceptions.ConnectionError):
                    print('error')
                    continue
                break

    # forge payload before post request
    def forge_payload(self, date, class_start=None, class_end=None):
        if (class_start != None and class_end != None):
            class_string = []
            for i in range(class_start, class_end + 1):
                class_string.append(str(i))
            final_class = "+".join(class_string)
            payload = "baseFr=on&objet=&classification={}&deposant=&mandataire=&numero=&dtedepot={}&classfig=\
            &sortList=4&nbResult=500&rechercher=Rechercher&recherche=recherche".format(
                final_class, date)
            return payload
        else:
            payload = "baseFr=on&objet=&classification=&deposant=&mandataire=&numero=&dtedepot={}&classfig=\
            &sortList=4&nbResult=500&rechercher=Rechercher&recherche=recherche".format(
                date)
            return payload

    # check if a variable is int or not
    def is_int(self, number):
        try:
            val = int(number)
            return val
        except ValueError:
            return False

    # post request to get number of companies
    def postman(self, threadID, date, class_start=None, class_end=None):

        url = "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_resultats_liste.html"

        payload = self.forge_payload(date, class_start, class_end)
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9",
            'Cache-Control': "no-cache",
            'connection': "keep-alive",
            'content-length': "183",
            'content-type': "application/x-www-form-urlencoded",
            'host': "bases-marques.inpi.fr",
            'origin': "https://bases-marques.inpi.fr",
            'referer': "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_recherche_avancee.html",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu \
            Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36",
        }

        response = self.s.request("POST", url, data=payload, headers=headers)
        text_response = response.text

        soup = BeautifulSoup(text_response,
                             features='html.parser')
        html_response = soup.prettify()

        with open(self.url_directory + date + '.txt', 'wb') as \
                my_file:
            my_file.write(html_response.encode('utf-8'))

        sel = Selector(text=html_response)
        company_number = 0
        try:
            company_number = sel.css(
                "div.csc-default:nth-child(2) div.tx-pitrechercheinpi-pi1:nth-child(1) form:nth-child(1) \
                div.txtresultats:nth-child(3) p:nth-child(1) > strong:nth-child(1)::text").extract()[
                0].strip()
            company_number = self.is_int(company_number)
        except:
            pass
        print(str(date) + " : spider-" + str(threadID))

        if company_number > 500:
            self.split_postman(date, self.threadID, 0, 10)
            self.split_postman(date, self.threadID, 11, 19)
            self.split_postman(date, self.threadID, 21, 27)
            self.split_postman(date, self.threadID, 28, 35)
            self.split_postman(date, self.threadID, 36, 45)
            return

        for i in range(1, company_number + 1):
            if i % 5 == threadID:
                self.detail_annonce(i, date)
            else:
                pass

    # same as postman, in case of too much results
    def split_postman(self, threadID, date, class_start=None, class_end=None):
        url = "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_resultats_liste.html"
        payload = self.forge_payload(date, class_start, class_end)
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9",
            'Cache-Control': "no-cache",
            'connection': "keep-alive",
            'content-length': "183",
            'content-type': "application/x-www-form-urlencoded",
            'host': "bases-marques.inpi.fr",
            'origin': "https://bases-marques.inpi.fr",
            'referer': "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_recherche_avancee.html",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu \
            Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36",
        }

        response = self.s.request("POST", url, data=payload, headers=headers)

        text_response = response.text

        soup = BeautifulSoup(text_response, 'html.parser')
        html_response = soup.prettify()

        with open(self.url_directory + date, 'wb') as \
                my_file:
            my_file.write(html_response)

        sel = Selector(text=html_response)
        try:
            company_number = sel.css(
                "div.csc-default:nth-child(2) div.tx-pitrechercheinpi-pi1:nth-child(1) form:nth-child(1) div.txtresult\
                ats:nth-child(3) p:nth-child(1) > strong:nth-child(1)::text").extract()[
                0].strip()
            company_number = self.is_int(company_number)

            for i in range(1, company_number + 1):
                if i % 5 == threadID:
                    self.detail_annonce(i, date)
                else:
                    pass
        except:
            pass

    # download detailed response in depository
    def detail_annonce(self, page_number, date):
        url = "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_fiche_resultats.html"
        querystring = {"index": page_number, "refId": "17877008_201811_ctmark", "y": "0"}
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9",
            'connection': "keep-alive",
            'host': "bases-marques.inpi.fr",
            'referer': "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_resultats_liste.html",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu \
            Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36",
            'Cache-Control': "no-cache",
        }
        response = self.s.request("GET", url, headers=headers, params=querystring)
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')
        html_response = soup.prettify()
        with open(self.url_directory + date + "_" +
                  str(page_number), 'wb') as my_file:
            my_file.write(html_response.encode('utf-8'))

    # enter on website
    def entry(self):

        url = "https://bases-marques.inpi.fr/Typo3_INPI_Marques/marques_recherche_avancee.html"

        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9",
            'connection': "keep-alive",
            'host': "bases-marques.inpi.fr",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/\
            64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36",
            'Cache-Control': "no-cache",
        }

        response = self.s.request("GET", url, headers=headers)

    # create dates
    def dates(self):
        date_table = []
        for i in range(self.starting_day, self.total_days+1):
            if i < 10:
                date = self.year + "-" + self.month + "-" + "0" + str(i)
                date_table.append(date)
            else:
                date = self.year + "-" + self.month + "-" + str(i)
                date_table.append(date)
        return date_table


threadLock = threading.Lock()

threadList = [
    "Thread-0",
    "Thread-1",
    "Thread-2",
    "Thread-3",
    "Thread-4"
]

threads = []
threadID = 0

# create new threads
for tName in threadList:
   thread = inpi_request(threadID, tName)
   thread.start()
   threads.append(thread)
   threadID = threadID + 1

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")
os.system('say "sasha tu es un champion"')