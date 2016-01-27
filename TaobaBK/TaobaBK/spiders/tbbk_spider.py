# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from TaobaBK.items import TaobabkItem

import codecs

class TBBKSpider(Spider):
    name = 'TBBK'

    allowed_domains = ['taobao.com']
    start_urls = [
        'http://s.taobao.com',
    ]

    def parse(self, response):
        #先进搜索首页
        if response.url == 'http://s.taobao.com':
            # "鼠标 无线"的搜索链接
            url = "https://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E9%BC%A0%E6%A0%87+%E6%97%A0%E7%BA%BF"

            yield Request(url, callback=self.parse)

        else:
            sel = Selector(response)

            # 不能工作
            all = sel.xpath('//div[@class="item"]/div[2]')

            #file = codecs.open('page.htm', 'wb', encoding='utf-8')
            #file.write(response.body.decode('unicode_escape'))

            for one in all:
                item = TaobabkItem()

                goods_price = one.xpath('div[1]/div[1]/strong/text()').extract()
                goods_sale_num = one.xpath('div[1]/div[@class="deal_cnt"]/text()').extract()
                # 提取数字
                goods_sale_num = "".join([s for s in goods_sale_num[0] if s.isdigit()])

                goods_name = one.xpath('div[2]/a/text()').extract()

                shop_name = one.xpath('div[3]/div[@class="shop"]/a/span[2]/text()').extract()
                shop_address = one.xpath('div[3]/div[@class="location"]/text()').extract()

                item['goods_price'] = goods_price
                item['goods_sale_num'] = goods_sale_num
                item['goods_name'] = [gn.encode('utf-8') for gn in goods_name]
                item['shop_name'] = [sn.encode('utf-8') for sn in shop_name]
                item['shop_address'] = [sa.encode('utf-8') for sa in shop_address]

                yield item

            next_page_urls = [
                'https://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E9%BC%A0%E6%A0%87+%E6%97%A0%E7%BA%BF&bcoffset=2&ntoffset=2&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=44',
                'https://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E9%BC%A0%E6%A0%87+%E6%97%A0%E7%BA%BF&bcoffset=-1&ntoffset=-1&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=88',
                'https://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E9%BC%A0%E6%A0%87+%E6%97%A0%E7%BA%BF&bcoffset=-4&ntoffset=-4&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=132',
                'https://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E9%BC%A0%E6%A0%87+%E6%97%A0%E7%BA%BF&bcoffset=-7&ntoffset=-7&p4plefttype=3%2C1&p4pleftnum=1%2C3&s=176'
            ]

            for next_page_url in next_page_urls:
                yield Request(next_page_url, callback=self.parse)




