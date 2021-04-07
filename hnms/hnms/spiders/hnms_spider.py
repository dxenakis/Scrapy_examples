import scrapy
import re
import scrapy.spiders
import datetime
from ..items import HnmsItem

class HnmsSpiderSpider(scrapy.Spider):
    name = 'hnms_spider'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    allowed_domains = ['http://www.hnms.gr/emy/el/observation/sa_teleytaies_paratiriseis_stathmou?perifereia=Peloponnese&poli=Tripoli']
    start_urls = ['http://www.hnms.gr/emy/el/observation/sa_teleytaies_paratiriseis_stathmou?perifereia=Peloponnese&poli=Tripoli']

    def parse(self, response):
        i=0
        crawldate    =  datetime.datetime.now() 
        table = response.xpath('//*[@class="table table-condensed table-striped table-hover small"]')
        rows = table.xpath('//tr')
        try:
            if (rows[1].xpath('td//text()')[27].extract()):
                    source      = 'Hnms.gr'
                    city        = 'Tripoli'
                    timestr     = rows[1].xpath('td//text()')[1].extract()
                    time        = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16]))  -  datetime.timedelta(hours=3, minutes=0)
                    temperature = float(rows[1].xpath('td//text()')[6].extract())
                    humidity    = float(rows[1].xpath('td//text()')[13].extract()[:-1])
                    wind        = float(((rows[1].xpath('td//text()')[27].extract().replace("\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t","")).replace("(","")).replace("kt)","") )*1.852
                    barometer   = 0
                    yetos       = 0
                    direction   = (rows[1].xpath('td//text()')[20].extract().replace("\n\t\t\t\t\t\t\t\t\t","")).replace("\n\t\t\t\t\t\t\t\t","").replace("\n\t\t\t\t\t\t\t","")
                    id          = source +' '+timestr
                    item = HnmsItem()
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

                

        except IndexError:
           
                    source      = 'Hnms.gr'
                    city        = 'Tripoli'
                    timestr     = rows[1].xpath('td//text()')[1].extract()
                    time        = datetime.datetime(int(timestr[6:10]), int(timestr[3:5]), int(timestr[0:2]),int(timestr[11:13]),int(timestr[14:16])) -  datetime.timedelta(hours=3, minutes=0)
                    temperature = float(rows[1].xpath('td//text()')[6].extract())
                    humidity    = float(rows[1].xpath('td//text()')[13].extract()[:-1])
                    #wind        = float(((rows[3].xpath('td//text()')[18].extract().replace("\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t","")).replace("(","")).replace("kt)","") )*1.852
                    windstr      = ((rows[1].xpath('td//text()')[15].extract().replace("\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t","")).replace("(","")).replace("kt)","")
                    print(windstr+'***************************')
                    if (windstr.strip() == 'ΑΠΝΟΙΑ'):
                        wind =0;
                    else:
                        wind     = float(((rows[1].xpath('td//text()')[18].extract().replace("\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t","")).replace("(","")).replace("kt)","") )*1.852
                    barometer   = 0
                    yetos       = 0
                    direction   = (rows[1].xpath('td//text()')[15].extract().replace("\n\t\t\t\t\t\t\t\t\t","")).replace("\n\t\t\t\t\t\t\t\t","").replace("\n\t\t\t\t\t\t\t","")
                    id          = source +' '+timestr
                    item = HnmsItem()
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
        yield scrapy.Request('http://www.hnms.gr/emy/el/observation/sa_teleytaies_paratiriseis_stathmou?perifereia=Peloponnese&poli=Tripoli', self.parse)
    
