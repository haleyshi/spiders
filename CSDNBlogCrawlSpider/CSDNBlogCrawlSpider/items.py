# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CsdnblogcrawlspiderItem(Item):
    blog_name = Field()
    blog_url = Field()
