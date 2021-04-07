import scrapy
import re
import scrapy.spiders
from ..items import MeteoItem
import datetime

class MeteoSpiderSpider(scrapy.Spider):
    name = 'meteo_spider'
    allowed_domains = ['http://penteli.meteo.gr/stations/tripoli/']
    start_urls = ['http://penteli.meteo.gr/stations/tripoli/']

    def parse(self, response):
        i=0
        table = response.xpath('//*[@id="table1"]')
        rows = table.xpath('//tr')
        source       = 'meteo.gr'
        city         = 'Tripoli'
        crawldate    =  datetime.datetime.now()
        timestr         = rows[2].xpath('td//text()')[3].extract()
        datepart     = timestr[-9:].strip()
        timepart     = timestr[2:-9].strip()
        datetimep    = datepart+' '+timepart
        #time         = datetime.datetime(int('20'+datetimep[6:8]), int(datetimep[3:5]), int(datetimep[0:2]),int(datetimep[9:11])-2,int(datetimep[12:14]))
        time         = datetime.datetime(int('20'+datetimep[6:8]), int(datetimep[3:5]), int(datetimep[0:2]),int(datetimep[-5:-3]),int(datetimep[-2:])) -   datetime.timedelta(hours=3, minutes=0)
        print(datepart)
        print(timepart)
        print(time)
        temperature  = float(rows[3].xpath('td//text()')[4].extract()[0:-2])
        humidity     = float(rows[4].xpath('td//text()')[4].extract()[:-1])
        windends     = (rows[6].xpath('td//text()')[4].extract()).find(" ")
        winddire     = (rows[6].xpath('td//text()')[4].extract()).find("at")
        wind         = float(rows[6].xpath('td//text()')[4].extract()[0:windends])
        barends      = rows[7].xpath('td//text()')[4].extract().find(" ")
        barometer    = float(rows[7].xpath('td//text()')[4].extract()[:barends])
        yetos        = float(rows[8].xpath('td//text()')[3].extract()[:-3])
        direction    = rows[6].xpath('td//text()')[4].extract()[winddire+3:]
        id           = source+' '+datetimep
        item = MeteoItem()
        item["id"]          = id
        item["source"]      = source
        item["time"]        = time
        item["timecrawl"]   = crawldate
        item["temperature"] = temperature
        item["humidity"]    = humidity
        item["wind"]        = wind
        item["barometer"]   = barometer
        item["yetos"]       = yetos
        item["direction"]   = direction
        item["city"]        = city
        yield item
        

    def start_requests(self):
        yield scrapy.Request('http://penteli.meteo.gr/stations/tripoli/', self.parse)
    
    