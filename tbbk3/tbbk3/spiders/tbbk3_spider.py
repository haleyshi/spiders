# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
#from scrapy.http.headers import Headers
#from scrapy.conf import settings

from tbbk3.items import Tbbk3Item
#from scrapyjs import SlotPolicy

#import codecs
#import json

class TBBKSpider(Spider):
    name = 'tbbk3'

    allowed_domains = ['taobao.com']
    start_urls = [
        'https://s.taobao.com',
    ]

    #iii = 0

    #def start_requests(self):
    #    for url in self.start_urls:
    #        body = json.dumps({'url': url, 'wait': 0.5})
    #        headers = Headers({'Content-Type': 'application/json'})

    #        yield Request(settings['SPLASH_RENDER_URL'], self.parse, method='POST', body=body, headers=headers)

    def parse(self, response):
        #先进搜索首页
        if response.url == 'https://s.taobao.com':
            # "鼠标 无线"的搜索链接
            url = "https://s.taobao.com/search?initiative_id=staobaoz_20120515&q=%E9%BC%A0%E6%A0%87+%E6%97%A0%E7%BA%BF"
            yield Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {
                        'wait': 0.5,
                    }

                    #'args': {
                    #    'html': 1,
                    #    'png': 1,
                        # 'url' is prefilled from request url
                    #},

                    #optional parameters
                    #'endpoint': 'render.json'   # this is default
                    #'splash_url': settings['SPLASH_RENDER_URL'], # can override SPLASH_URL
                    #'slot_policy': SlotPolicy.PER_DOMAIN    #default, Concurrency & politeness: PER_DOMAIN, SINGLE_SLOT, SCRAPY_DEFAULT
                }
            })

        else:
            sel = Selector(response)

            # 不能工作
            all = sel.xpath('//div[@class="item  "]/div[2]')

            #file = codecs.open('page_'+str(self.iii)+'.htm', 'wb', encoding='utf-8')
            #file.write(response.body.decode('unicode_escape'))
            #self.iii += 1

            #print all

            for one in all:
                item = Tbbk3Item()

                goods_price = one.xpath('div[1]/div[1]/strong/text()').extract()

                #print goods_price
                goods_sale_num = one.xpath('div[1]/div[@class="deal-cnt"]/text()').extract()

                #print goods_sale_num
                # 提取数字
                if len(goods_sale_num) > 0:
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
                yield Request(next_page_url, self.parse, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': {
                            'wait': 0.5,
                        },
                    }
                })




