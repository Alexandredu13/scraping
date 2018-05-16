from bs4 import BeautifulSoup
import os
from scrapy import Selector
import urllib.request
import threading


class spider(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.count = 0
        self.directory_name = "042018"
        self.limit = 2300

    def increment(self):
        self.count = self.count + 1

    def run(self):
        path = '/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/inpi/main_page_requests/' + self.directory_name

        for filename in os.listdir(path):

            if self.count >= self.limit:

                with open(path+"/"+filename, "r") as html_page:
                    soup = BeautifulSoup(html_page,
                                         features='html.parser')
                    sel = Selector(text=soup.prettify())

                    if self.count % 3 == self.threadID:

                        logo_name = ('logo_%s' % self.count).encode('utf-8')

                        image_urls = sel.xpath('//img[@class="null"]/@src').extract_first()
                        if image_urls is not None:
                            image_urls = 'https://bases-marques.inpi.fr/' + image_urls
                            urllib.request.urlretrieve(image_urls,
                                                       "/Users/sashabouloudnine/PycharmProjects/lobstr/scraping/inpi/logos/" + self.directory_name+ "/%s.png" % logo_name)

                        else:
                            pass

                        print('-- SUCCESS : %s --' % logo_name)
                        spider.increment(self)

                    else:
                        spider.increment(self)
                        pass

            else:
                spider.increment(self)
                print(self.count)
                pass

threadList = [
    "Thread-0",
    "Thread-1",
    "Thread-2"
]

threads = []
threadID = 0

# create new threads
for tName in threadList:
   thread = spider(threadID, tName)
   thread.start()
   threads.append(thread)
   threadID = threadID + 1

for t in threads:
    t.join()
print("Exiting Main Thread")
os.system('say "travail terminai"')
