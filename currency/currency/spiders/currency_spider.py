# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector

from currency.items import CurrencyItem

class CurrencySpider(Spider):
    name = "currency"
    allowed_domains = ['www.boc.cn']
    start_urls = [
        'http://www.boc.cn/sourcedb/whpj/index.html'
    ]

    def parse(self, response):
        sel = Selector(response)

        sites = sel.xpath('//table[@align="left"]/tr')

        items = []

        for site in sites:
            item = CurrencyItem()

            currency = site.xpath('td[1]/text()').extract()
            value = site.xpath('td[6]/text()').extract()
            date = site.xpath('td[7]/text()').extract()
            time = site.xpath('td[8]/text()').extract()

            item['currency'] = [c.encode('utf-8') for c in currency]
            item['value'] = value
            item['date'] = date
            item['time'] = time

            items.append(item)

            #print item

        return items

