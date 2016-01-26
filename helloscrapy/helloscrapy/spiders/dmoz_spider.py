# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from helloscrapy.items import DmozItem

class DmozSpider(Spider):
    name = 'dmoz'
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')

        items = []

        for site in sites:
            item = DmozItem()
            item["name"] = site.xpath('a/text()').extract()
            item["url"] = site.xpath('a/@href').extract()
            item["description"] = site.xpath('text()').re('-\s[^\n]*\\r')

            items.append(item)

        return items