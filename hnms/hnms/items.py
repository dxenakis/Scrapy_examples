# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HnmsItem(scrapy.Item):
    id           = scrapy.Field()
    source 	 = scrapy.Field()
    time 	 = scrapy.Field()
    timecrawl    = scrapy.Field()
    temperature  = scrapy.Field()
    humidity     = scrapy.Field()
    wind         = scrapy.Field()
    barometer    = scrapy.Field()
    yetos        = scrapy.Field()
    direction    = scrapy.Field()
    city         = scrapy.Field()
