import scrapy
from datetime import datetime as dt
from datetime import date
import datetime
from ..items import XalaziItem

class XalaziSpiderSpider(scrapy.Spider):
    name = 'xalazi_spider'
    allowed_domains = ['http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178']
    start_urls = ['http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178']
    
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
    
    def parse_fog(self, response):
        fog = 'omixli'
        return fog
    def parse(self, response):
        
        source       = 'xalazi.gr'
        city         = 'Tripoli'
        #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
        hour         =  response.xpath('//*[@class="t orangered"]/tr[1]/td[2]//text()').get().replace("\r","").replace("\n","").strip()[:2]
        hour         =  int(self.timeStrToInt(hour))
        crawldate    =  dt.now() 
        if (hour == 0):
            cdate        =  dt.now() #+  datetime.timedelta(days = 1)
        else:
            cdate        =  dt.now()
        year         =  int(cdate.year)
        month        =  int(self.timeStrToInt(response.xpath('//*[@class="t orangered"]/tr[1]/td[1]//text()')[1].get().replace("\r","").replace("\n","").strip()[3:]))
        day          =  int(self.timeStrToInt(response.xpath('//*[@class="t orangered"]/tr[1]/td[1]//text()')[1].get().replace("\r","").replace("\n","").strip()[:2]))
        
        time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=3, minutes=0)
        timeutc      =  dt(year, month,day,int(hour),0)
        timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
        temperature  =  float(response.xpath('//*[@class="t orangered"]/tr[1]/td[3]//text()').get().replace("\r","").replace("\n","").strip()[:-2])
        humidity     =  float(response.xpath('//*[@class="t orangered"]/tr[1]/td[4]//text()').get().replace("\r","").replace("\n","").strip()[:-1])
        #windends    = (rows[6].xpath('td//text()')[4].extract()).find(" ")
        #winddire    = (rows[6].xpath('td//text()')[4].extract()).find("at")
        barometer    =  float()
        yetos_index  =  int()
        yetos        =  float()
        windindex    =  int(response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().find(" "))
        direction    =  response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().replace("\r","").replace("\n","")[windindex:].strip()
        b            =  int(response.xpath('//*[@class="t orangered"]/tr[1]/td[5]//text()').get().replace("\r","").replace("\n","")[:windindex].strip())
        wind         =  float(self.bofortToKm(b))
        #barends     = rows[7].xpath('td//text()')[4].extract().find(" ")
        
        
        
        
        id           =  source+' '+timestr
        item = XalaziItem()
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
        
        #yield scrapy.Request('http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178',self.parse_fog)
        yield item



    def start_requests(self):
        yield scrapy.Request('http://www.xalazi.gr/prognwsh-kairou/prognosi-5-imeron?type=FiveDays&city=1178', self.parse)

