# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import influxdb


class CoinspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CoinsItem(scrapy.Item):
    url = scrapy.Field()
    user = scrapy.Field()
    email = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field()
    require_min = scrapy.Field()
    require_max = scrapy.Field()
    trade_bank = scrapy.Field()
    trade_method = scrapy.Field()
    trade_msg = scrapy.Field()
    trade_location = scrapy.Field()
    time = scrapy.Field()
