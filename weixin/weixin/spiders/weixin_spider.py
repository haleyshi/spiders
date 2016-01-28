# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector

from weixin.items import WeixinItem

class WeixinSpide(Spider):
    name = 'weixin'
    allowed_domains = []
    start_urls = [
        'http://weixin.sogou.com'
    ]


    def parse(self, response):
        sel = Selector(response)

        list = sel.xpath('//div[@class="wx-news-info2"]')

        for article in list:
            item = WeixinItem()

            title = article.xpath('a/text()').extract()
            link = article.xpath('a/@href').extract()

            item['title'] = [t.encode('utf-8') for t in title]
            item['link'] = link

            yield item