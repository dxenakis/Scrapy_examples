import scrapy
import re
import scrapy.spiders
from ..items import AccweatherItem
from datetime import datetime as dt
from datetime import date
import datetime
import json
import time
import urllib.request



class AccspiderSpider(scrapy.Spider):
    name = 'accspider'
    allowed_domains = ['https://www.accuweather.com/el/gr/tripoli/182060/current-weather/182060']
    start_urls = ['https://www.accuweather.com/el/gr/tripoli/182060/current-weather/182060']
    API = "RRJyGGJLmKpqWE0R0hc1N0vUWPUXygdG"
    LOCATION_ID = "182060"
    
    def parse(self, response):
        API = "RRJyGGJLmKpqWE0R0hc1N0vUWPUXygdG"
        LOCATION_ID = "182060"
        table = response.xpath('//*[@id="table1"]')
        rows = table.xpath('//tr')
        source       = 'accuweather.com'
        crawldate    =  dt.now() 
        cdate        = dt.now() 
        time         =  cdate - datetime.timedelta(hours=3, minutes=0)
        timestr       = cdate.strftime("%d/%m/%Y, %H:%M")
        timestamp = time.time()
        url = 'http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true' % (LOCATION_ID, API)
        print(url)
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
        #print(data)
        temperature = float(((data[0]['Temperature']['Imperial']['Value']) -30 )/2)
        humidity    = float(data[0]['RelativeHumidity'])
        direction   = data[0]['Wind']['Direction']['English']
        wind        = float((data[0]['Wind']['Speed']['Metric']['Value'])*1) #.60934
        #data[0]['UVIndex'],
        #data[0]['CloudCover'],
        barometer   = float(data[0]['Pressure']['Metric']['Value'])
        yetos       = float(data[0]['Precip1hr']['Metric']['Value'])
        id           = source+' '+timestr
        city         = 'Tripoli'
        item = AccweatherItem()
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
        yield scrapy.Request('https://www.accuweather.com/el/gr/tripoli/182060/current-weather/182060', self.parse)

    
