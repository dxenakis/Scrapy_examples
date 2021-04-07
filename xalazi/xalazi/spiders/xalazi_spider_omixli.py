import scrapy


class XalaziSpiderOmixliSpider(scrapy.Spider):
    name = 'xalazi_spider_omixli'
    allowed_domains = ['xalazi.gr']
    start_urls = ['http://xalazi.gr/']

    def parse(self, response):
        pass
