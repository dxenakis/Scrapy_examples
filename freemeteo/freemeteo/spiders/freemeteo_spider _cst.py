import scrapy
import re
import scrapy.spiders
from ..items import FreemeteoItem
from datetime import datetime as dt
from datetime import date
import datetime

class FreemeteoSpiderSpider(scrapy.Spider):
    name = 'freemeteo_spider_cst'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    allowed_domains = ['https://freemeteo.gr/kairos/tripoli/oriaia-provlepsi/simera/?gid=252601&language=greek&country=greece']
    start_urls = ['https://freemeteo.gr/kairos/tripoli/oriaia-provlepsi/simera/?gid=252601&language=greek&country=greece']
    

    def parse(self, response):
        i=1
        timelisttoday    = ['23']#,['08', '11', '14', '17', '20', '23']
        timelisttommorow = ['']#,['02', '05']
        table = response.xpath('//*[@class="today table"]')
        rows = table.xpath('//tbody//tr')
        
        for itemtime in timelisttoday:
            source       = 'freemeteo.gr'
            city         = 'Tripoli'
            #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
            cdate        =  dt.now()  #print(now.year, now.month, now.day, now.hour, now.minute, now.second)
            year         =  cdate.year
            month        =  cdate.month
            day          =  cdate.day
            hour         =  itemtime
            time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=2, minutes=0)
            timeutc      =  dt(year, month,day,int(hour),0)
            timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
            temperature  =  float(5)
            humidity     =  float(92)
            #windends     = (rows[6].xpath('td//text()')[4].extract()).find(" ")
            #winddire     = (rows[6].xpath('td//text()')[4].extract()).find("at")
            barometer    =  float(1026.1)
            print('*********************************')
            print(i)
            wind         =  float(1)
            #barends      = rows[7].xpath('td//text()')[4].extract().find(" ")
            
            yetos        =  float(0.0)
            direction    =  ''
            i            =  i + 1
            if ( barometer > 0  ):
                id           =  source+' '+timestr
                item = FreemeteoItem()
                item["id"]          = id
                item["source"]      = source
                item["time"]        = time
                item["temperature"] = temperature
                item["humidity"]    = humidity
                item["wind"]        = wind
                item["barometer"]   = barometer
                item["yetos"]       = yetos
                item["direction"]   = direction
                item["city"]        = city
                yield item
        
        
        for itemtime in timelisttommorow:
            source       = 'freemeteo.gr'
            city         = 'Tripoli'
            #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
            cdate        =  dt.now()  + datetime.timedelta(days = 1)   #print(now.year, now.month, now.day, now.hour, now.minute, now.second)
            year         =  cdate.year
            month        =  cdate.month
            day          =  cdate.day
            hour         =  itemtime
            time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=2, minutes=0)
            timeutc      =  dt(year, month,day,int(hour),0)
            timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
            temperature  =  float(4)
            humidity     =  float(93)
            #windends     = (rows[6].xpath('td//text()')[4].extract()).find(" ")
            #winddire     = (rows[6].xpath('td//text()')[4].extract()).find("at")
            barometer    =  float(1025.5)
            print('*********************************')
            print(i)
            wind         =  float(1)
            #barends      = rows[7].xpath('td//text()')[4].extract().find(" ")
            
            yetos        =  float(0)
            direction    =  ''
            i            =  i + 1
            if ( barometer > 0  ):
                id           =  source+' '+timestr
                item = FreemeteoItem()
                item["id"]          = id
                item["source"]      = source
                item["time"]        = time
                item["temperature"] = temperature
                item["humidity"]    = humidity
                item["wind"]        = wind
                item["barometer"]   = barometer
                item["yetos"]       = yetos
                item["direction"]   = direction
                item["city"]        = city
                yield item
                



    def start_requests(self):
        yield scrapy.Request('https://freemeteo.gr/kairos/tripoli/oriaia-provlepsi/simera/?gid=252601&language=greek&country=greece', self.parse)
        
    
        
        
        
        
        


