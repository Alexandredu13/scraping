import requests
from scrapy import Selector
from bs4 import BeautifulSoup


class spider():

    def __init__(self):
        self.r = requests.Session()

    def requests(self):
        index_page = self.r.get('http://www.cenior.fr/repertoire/', allow_redirects=False)
        spider.bs(self, index_page)


    def bs(self, page):
        soup = BeautifulSoup(page, features='html.parser')
        sel = Selector(text=soup.prettify())
        return sel



'''                    soup = BeautifulSoup(html_page,
                                         features='html.parser',
                                         from_encoding='utf-8'
                                         )
                    sel = Selector(text=soup.prettify())
'''