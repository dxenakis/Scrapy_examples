import scrapy
from datetime import datetime as dt
from datetime import date
import datetime
from ..items import OkairosItem

class OkairosSpiderSpider(scrapy.Spider):
    name = 'okairos_spider'
    allowed_domains = ['https://www.okairos.gr/%CF%84%CF%81%CE%AF%CF%80%CE%BF%CE%BB%CE%B7.html?v=%CF%89%CF%81%CE%B9%CE%B1%CE%AF%CE%B1']
    start_urls = ['https://www.okairos.gr/%CF%84%CF%81%CE%AF%CF%80%CE%BF%CE%BB%CE%B7.html?v=%CF%89%CF%81%CE%B9%CE%B1%CE%AF%CE%B1']
    
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
    
    def timeStrToInt(self,b):
        switcher = {
            "00": 0,
            "01": 1,
            "02": 2,
            "03": 3,
            "04": 4,
            "05": 5,
            "06": 6,
            "07": 7,
            "08": 8,
            "09": 9,
            
            
        }
        return switcher.get(b, b)
        
        

    def parse(self, response):
        
        source       = 'okairos.gr'
        city         = 'Tripoli'
        #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
        hour         =  response.xpath('//*[@class="wnfp"]/table[1]/tr[2]/td[1]/text()').get()[0:2] 
        hour         =  int(self.timeStrToInt(hour))
        crawldate    =  dt.now() 
        if (hour == 0):
            cdate        =  dt.now() +  datetime.timedelta(days = 1)
        else:
            cdate        =  dt.now()
        year         =  cdate.year
        month        =  cdate.month
        day          =  cdate.day
        
        time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=3, minutes=0)
        timeutc      =  dt(year, month,day,int(hour),0)
        timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
        temperature  =  float(response.xpath('//*[@class="wnfp"]/table[1]/tr[2]/td[3]/div/text()').get()[:-1])
        humidity     =  float(response.xpath('//*[@class="wnfp"]/table[1]/tr[2]/td[9]/text()').get()[:-1])
        #windends    = (rows[6].xpath('td//text()')[4].extract()).find(" ")
        #winddire    = (rows[6].xpath('td//text()')[4].extract()).find("at")
        barometer    =  float(response.xpath('//*[@class="wnfp"]/table[1]/tr[2]/td[10]/text()').get().replace("\n","").replace("\t","")[:-4])
        yetos        =  float(response.xpath('//*[@class="wnfp"]/table[1]/tr[2]/td[7]/text()').get().replace("\t","").replace(",",".")[:-2])
        direction    =  'null'
        b            =  int(response.xpath('//*[@class="wnfp"]/table[1]/tr[2]/td[5]/text()').get().strip())
        wind         =  float(self.bofortToKm(b))
        #barends     = rows[7].xpath('td//text()')[4].extract().find(" ")
        
        id           =  source+' '+timestr
        item = OkairosItem()
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
        yield scrapy.Request('https://www.okairos.gr/%CF%84%CF%81%CE%AF%CF%80%CE%BF%CE%BB%CE%B7.html?v=%CF%89%CF%81%CE%B9%CE%B1%CE%AF%CE%B1', self.parse)