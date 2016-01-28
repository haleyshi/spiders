# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Tbbk2Item(Item):
    shop_name = Field()
    shop_address = Field()
    goods_name = Field()
    goods_price = Field()
    goods_sale_num = Field()