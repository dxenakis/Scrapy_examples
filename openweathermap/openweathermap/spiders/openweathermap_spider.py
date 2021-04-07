import scrapy
import re
import scrapy.spiders
from ..items import OpenweathermapItem
from datetime import datetime as dt
from datetime import date
import datetime
import json
import time
import urllib.request


class OpenweathermapSpiderSpider(scrapy.Spider):
    name = 'openweathermap_spider'
    allowed_domains = ['https://openweathermap.org/city/252601']
    start_urls = ['https://openweathermap.org/city/252601']
    API = "1710e8d0a7f075fa96641c63765dd296"
    LOCATION_ID = "182060"
    
    def parse(self, response):
        API = "RRJyGGJLmKpqWE0R0hc1N0vUWPUXygdG"
        LOCATION_ID = "252601"
        table = response.xpath('//*[@id="table1"]')
        rows = table.xpath('//tr')
        source       = 'openweathermap.org'
        crawldate    =  dt.now() 
        cdate        =  dt.now() 
        time         =  cdate - datetime.timedelta(hours=3, minutes=0)
        timestr       = cdate.strftime("%d/%m/%Y, %H:%M")
        timestamp = time.time()
        url = 'http://api.openweathermap.org/data/2.5/weather?id=252601&appid=1710e8d0a7f075fa96641c63765dd296&units=metric'
        print(url)
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
        #print(data)
        temperature = float(data['main']['temp'])
        humidity    = float(data['main']['humidity'])
        direction   = data['wind']['deg']
        wind        = float(data['wind']['speed'])*3.6
        #data[0]['UVIndex'],
        #data[0]['CloudCover'],
        barometer   = float(data['main']['pressure'])
        yetos       = float()
        id           = source+' '+timestr
        city         = 'Tripoli'
        item = OpenweathermapItem()
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
        yield scrapy.Request('https://openweathermap.org/city/252601', self.parse)







