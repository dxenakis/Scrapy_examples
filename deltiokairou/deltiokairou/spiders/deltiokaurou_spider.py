import scrapy
from datetime import datetime as dt
from datetime import date
import datetime
from ..items import DeltiokairouItem


class DeltiokaurouSpiderSpider(scrapy.Spider):
    name = 'deltiokaurou_spider'
    allowed_domains = ['https://www.deltiokairou.gr/gr/weather/arkadia/tripoli/tripoli/']
    start_urls = ['https://www.deltiokairou.gr/gr/weather/arkadia/tripoli/tripoli/']
    
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
        
        source       = 'deltiokairou.gr'
        city         = 'Tripoli'
        #time         = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=2, minutes=0)
        hour         =  response.xpath('//*[@class="multicolor fixed"]/tbody/tr/td[1]/text()')[1].get()[:-3]
        hour         =  int(self.timeStrToInt(hour))
        crawldate    =  dt.now() 
        if (hour == 0):
            cdate        =  dt.now() #+  datetime.timedelta(days = 1)
        else:
            cdate        =  dt.now()
        year         =  int(response.xpath('//*[@class="date-box"]').get()[33:37])
        month        =  int(response.xpath('//*[@class="date-box"]').get()[38:40])
        day          =  int(response.xpath('//*[@class="date-box"]').get()[41:43])
        
        time         =  dt(year, month,day,int(hour),0)  -   datetime.timedelta(hours=3, minutes=0)
        timeutc      =  dt(year, month,day,int(hour),0)
        timestr      =  timeutc.strftime("%d/%m/%Y, %H:%M")
        temperature  =  float(response.xpath('//*[@class="multicolor fixed"]/tbody/tr/td[3]/text()').get()[:-2])
        humidity     =  float()
        #windends    = (rows[6].xpath('td//text()')[4].extract()).find(" ")
        #winddire    = (rows[6].xpath('td//text()')[4].extract()).find("at")
        barometer    =  float()
        yetos_index  =  int(response.xpath('//*[@id="content"]/section[1]/div[1]/div[1]/div/div/div[1]/div[2]/p/text()')[2].get().replace("\r","").replace("\n","").strip().find("mm"))
        yetos        =  float(response.xpath('//*[@id="content"]/section[1]/div[1]/div[1]/div/div/div[1]/div[2]/p/text()')[2].get().replace("\r","").replace("\n","").strip()[:yetos_index-1])
        dirindex     =  int(response.xpath('//*[@id="content"]/section[1]/div[1]/div[1]/div/div/div[1]/div[2]/p/text()[4]').get().find("-"))
        direction    =  response.xpath('//*[@id="content"]/section[1]/div[1]/div[1]/div/div/div[1]/div[2]/p/text()[4]').get()[:dirindex-1].strip().replace("\xa0"," ") 
        b            =  int(response.xpath('//*[@class="multicolor fixed"]/tbody/tr/td[4]/span/text()').get()[2:].strip())
        wind         =  float(self.bofortToKm(b))
        #barends     = rows[7].xpath('td//text()')[4].extract().find(" ")
        
        id           =  source+' '+timestr
        item = DeltiokairouItem()
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
        yield scrapy.Request('https://www.deltiokairou.gr/gr/weather/arkadia/tripoli/tripoli/', self.parse)
