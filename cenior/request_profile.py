import requests
import urllib
from bs4 import BeautifulSoup
import os
import re
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import re
import codecs
import csv
import sys
import time
import threading
import Queue
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')

exitFlag = 0

class spider(threading.Thread):

    def __init__(self, id, name, q):
        self.last_url = 'entrepreneur-yernaux-electricie-bricolage-plomberie-corquoy-757.htm.txt'
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.q = q
        self.path = "/Users/sashabouloudnine/PycharmProjects/scraping/sandbox/cenior/profiles/"
        self.r = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.cenior.fr',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/65.0.3325.181 Safari/537.36'
        }

    def run(self):
        print "Starting " + self.name
        spider.process_data(self, self.q)
        print "Exiting " + self.name

    def process_data(self, q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                spider.request_page(self, data)
            else:
                queueLock.release()
            time.sleep(1)

    def request_page(self, url):
        rep0 = self.r.get(url, headers=self.headers, allow_redirects=False)
        text_response = rep0.text
        soup = BeautifulSoup(text_response, features='html.parser')
        html_response = soup.prettify()

        name = url.replace('http://www.cenior.fr/', '').replace('/', '-')
        with open(self.path + name + '.txt', 'w') as my_file:
            my_file.write(html_response)
        print '-- SUCCESS : %s' % name

threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5"]
db = pd.read_csv("/Users/sashabouloudnine/PycharmProjects/scraping/sandbox/cenior/urls.csv", delimiter="$")
queueLock = threading.Lock()
workQueue = Queue.Queue()
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = spider(id, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1
print 'threads done'

# Fill the queue
queueLock.acquire()
for i in db['url']:
   workQueue.put('http://www.cenior.fr/' + i)
   print 'http://www.cenior.fr/' + i
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print "Exiting Main Thread"

