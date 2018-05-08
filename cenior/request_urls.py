import requests
import csv
from scrapy import Selector
from bs4 import BeautifulSoup
import datetime


class SpiderCenior():

    def __init__(self):
        self.r = requests.Session()
        self.fieldnames = ['url']

    def extract(self):
        time = []
        a = datetime.datetime.now()
        time.append(a)
        with open('urls_cenior.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

            for i in range(0, 3091):
                response = self.r.get('http://www.cenior.fr/repertoire/%s/le-repertoire-des-entrepreneurs.htm' % i)
                print response.status_code
                response = response.text
                soup = BeautifulSoup(response, features='html.parser')
                sel = Selector(text=soup.prettify())


                urls = sel.xpath("//div[@class='result-right-col']//a/@href").extract()
                for j in urls:
                    j = j.encode('utf-8')
                    writer.writerow({'url': j})
                print "Page done : %s" % i
                b = datetime.datetime.now()
                time.append(b)
                c = (b-a).total_seconds()
                rmt = (c * 3091 - i) / 60
                prct = 100 * i / 3091
                prct = str(prct)
                print 'Minutes remaining : %s' % rmt
                print '%s' % prct + '%'
                a = b


spider = SpiderCenior()
spider.extract()


'''
soup = BeautifulSoup(html_page,
features='html.parser',
from_encoding='utf-8'
                                         )
sel = Selector(text=soup.prettify())
'''