import scrapy
import re
import scrapy.spiders
from ..items import FreemeteoItem
from datetime import datetime as dt
from datetime import date
import datetime

class FreemeteoSpiderSpider(scrapy.Spider):
    name = 'freemeteo_spider'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    allowed_domains = ['https://freemeteo.gr/kairos/tripoli/oriaia-provlepsi/simera/?gid=252601&language=greek&country=greece']
    start_urls = ['https://freemeteo.gr/kairos/tripoli/oriaia-provlepsi/simera/?gid=252601&language=greek&country=greece']
    
    def bofortToKm(self,b):
        switcher = {
          0: 1,
          1: 3.5,
          2: 8,
          3: 16,
          4: 25,
          5: 33,
          6: 45,
          7: 56,
          8: 69,
          9: 80,
          10: 96,
          11: 110,
          12: 124
        }
        return switcher.get(b, 0)
    

    def parse(self, response):
        i=1
        timelisttoday    = ['08', '11', '14', '17', '20', '23']
        timelisttommorow = ['02', '05']
        table = response.xpath('//*[@class="today table"]')
        rows = table.xpath('//tbody//tr')
        crawldate    =  dt.now() 
        for itemtime in timelisttoday:
            source       = 'freemeteo.gr'
            city         = 'Tripoli'
            #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
            cdate        =  dt.now()  #print(now.year, now.month, now.day, now.hour, now.minute, now.second)
            year         =  cdate.year
            month        =  cdate.month
            day          =  cdate.day
            hour         =  itemtime
            time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=3, minutes=0)
            timeutc      =  dt(year, month,day,int(hour),0)
            timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
            temperature  =  float((rows[2].xpath('td//text()')[i].extract()).replace("\xa0","000")[0:-2])
            humidity     =  float((rows[5].xpath('td//text()')[i].extract()).replace("\xa0","00")[:-1])
            #windends     = (rows[6].xpath('td//text()')[4].extract()).find(" ")
            #winddire     = (rows[6].xpath('td//text()')[4].extract()).find("at")
            barometer    =  float(((rows[6].xpath('td//text()')[i].extract()).replace(",",".")).replace("\xa0","000")[:-2])
            print('*********************************')
            print(i)
            #self.bofortToKm(b)
            b             =  int((rows[4].xpath('td//text()')[i*2].extract()).replace("\xa0","0000")[:-3])
            wind          =  float(self.bofortToKm(b))
            #barends      = rows[7].xpath('td//text()')[4].extract().find(" ")
            
            yetos        =  float( ((rows[7].xpath('td//text()')[i].extract()).replace("\xa0","000")[:-2]).replace(",","."))
            direction    =  ''
            i            =  i + 1
            if ( barometer > 0  ):
                id           =  source+' '+timestr
                item = FreemeteoItem()
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
        
        
        for itemtime in timelisttommorow:
            
            source       = 'freemeteo.gr'
            city         = 'Tripoli'
            #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
            cdate        =  dt.now()  + datetime.timedelta(days = 1)   #print(now.year, now.month, now.day, now.hour, now.minute, now.second)
            year         =  cdate.year
            month        =  cdate.month
            day          =  cdate.day
            hour         =  itemtime
            time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=3, minutes=0)
            timeutc      =  dt(year, month,day,int(hour),0)
            timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
            temperature  =  float((rows[2].xpath('td//text()')[i].extract()).replace("\xa0","000")[0:-2])
            humidity     =  float((rows[5].xpath('td//text()')[i].extract()).replace("\xa0","00")[:-1])
            #windends     = (rows[6].xpath('td//text()')[4].extract()).find(" ")
            #winddire     = (rows[6].xpath('td//text()')[4].extract()).find("at")
            barometer    =  float(((rows[6].xpath('td//text()')[i].extract()).replace(",",".")).replace("\xa0","000")[:-2])
            print('*********************************')
            print(i)
            b             =  int((rows[4].xpath('td//text()')[i*2].extract()).replace("\xa0","0000")[:-3])
            wind          =  float(self.bofortToKm(b))
            #barends      = rows[7].xpath('td//text()')[4].extract().find(" ")
            
            yetos        =  float( ((rows[7].xpath('td//text()')[i].extract()).replace("\xa0","000")[:-2]).replace(",","."))
            direction    =  ''
            i            =  i + 1
            if ( barometer > 0  ):
                id           =  source+' '+timestr
                item = FreemeteoItem()
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
        yield scrapy.Request('https://freemeteo.gr/kairos/tripoli/oriaia-provlepsi/simera/?gid=252601&language=greek&country=greece', self.parse)
        
    
        
        
        
        
        


