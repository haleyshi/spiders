# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from CSDNBlogCrawlSpider.items import CsdnblogcrawlspiderItem

class CSDNBlogCrawlSpider(CrawlSpider):
    """自动爬取链接的爬虫"""

    name = 'CSDNBlogCrawlSpider'

    allowed_domains = ['blog.csdn.net']

    start_urls = [
        'http://blog.csdn.net/u012150179/article/details/11749017'
    ]

    rules = [
        Rule(LinkExtractor(allow=('/u012150179/article/details'),
                               restrict_xpaths=('//li[@class="next_article"]')),
             callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        item = CsdnblogcrawlspiderItem()

        sel = Selector(response)

        blog_url = str(response.url)
        blog_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()

        item['blog_name'] = [bn.encode('utf-8') for bn in blog_name]
        item['blog_url'] = blog_url.encode('utf-8')

        yield item

