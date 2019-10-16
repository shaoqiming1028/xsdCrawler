# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class xsdItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    cid = scrapy.Field()
    brand = scrapy.Field()
    imagediv = scrapy.Field()
    image = scrapy.Field()
