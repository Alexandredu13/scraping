import scrapy
from scrapy.crawler import CrawlerProcess
# from scrapy.exceptions import DropItem
import json
import os
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst
clean_text = Compose(MapCompose(lambda v: v.strip()), Join())
from w3lib.html import remove_tags

# counter
count = 0
def increment():
    global count
    count = count+1
    print(count)

# forge url_table
url_table = []
path = "/Users/sashabouloudnine/Desktop/main_page_requests"
for file in os.listdir(path):
    file = 'file:///Users/sashabouloudnine/Desktop/main_page_requests/' + file
    url_table.append(file)

# item
class InpiItem(scrapy.Item):
    marque = scrapy.Field()
    classification = scrapy.Field()
    deposant = scrapy.Field()
    mandataire = scrapy.Field()
    numero = scrapy.Field()
    date = scrapy.Field()
    logo_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

# spider
class SpiderLocal(scrapy.Spider):
    name = 'spider_local'
    start_urls = url_table

    def parse(self, response):
        l = ItemLoader(item=InpiItem(), response=response)
        l.add_xpath('marque', '//div[@class="blanc"]/div/p[contains(strong, "Marque")]/text()')
        l.add_xpath('classification', '//div[@class="blanc"]/div/p[contains(strong, "Classification de Nice")]/text()')
        l.add_xpath('deposant', '//div[@class="blanc"]/div/p[contains(strong, "posant")]/text()')
        l.add_xpath('mandataire', '//div[@class="blanc"]/div/p[contains(strong, "Mandataire")]/text()')
        l.add_xpath('numero', '//div[@class="blanc"]/div/p[contains(strong, "Num")]/text()')
        l.add_xpath('date', '//div[@class="blanc"]/div/p[contains(strong, "Date de")]/text()')
        l.add_value('logo_name', 'logo_%s' % count)
        l.add_xpath('image_urls', '//img[@class="null"]/@src')
        yield l.load_item()
        increment()

# json writer
class JsonWriterPipeline(object):

    def open_spider(self, SpiderLocal):
        self.file = open('items.json', 'w')

    def close_spider(self, SpiderLocal):
        self.file.close()

    def process_item(self, InpiItem, SpiderLocal):
        line = json.dumps(dict(InpiItem)) + "\n"
        self.file.write(line)
        return InpiItem

# lancement
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'ITEM_PIPELINES': { '__main__.JsonWriterPipeline': 100},
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(SpiderLocal)
process.start() # the script will block here until the crawling is finished
