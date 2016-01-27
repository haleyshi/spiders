# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from CSDNBlog.items import CsdnblogItem

class CSDNBlogSpider(Spider):
    name = "CSDNBlog"

    #download_delay = 1
    allowed_domains = ['blog.csdn.net']

    start_urls = [
        'http://blog.csdn.net/u012150179/article/details/11749017'
    ]

    def parse(self, response):
        sel = Selector(response)

        item = CsdnblogItem()

        article_url = str(response.url)
        article_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()

        item['article_name'] = [an.encode('utf-8') for an in article_name]
        item['article_url'] = article_url.encode('utf-8')

        yield item

        urls = sel.xpath('//li[@class="next_article"]/a/@href').extract()

        for url in urls:
            url = 'http://blog.csdn.net' + url
            yield Request(url, callback=self.parse)