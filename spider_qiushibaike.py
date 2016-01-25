# -*- coding: utf-8 -*-

import urllib, urllib2
import re
import thread, time

class Spider_Model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False

    def GetPage(self, page):
        myUrl = "http://m.qiushibaike.com/hot/page/" + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent' : user_agent}
        req = urllib2.Request(url=myUrl, headers=headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")

        #找出所有 class="content"的div标记
        myItems = re.findall(r'<div.*?class="content">(.*?)</div>', unicodePage, re.S)
        items = []
        for item in myItems:
            items.append(item.replace("\n", ""))

        return items

    def LoadPage(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.GetPage(str(self.page))

                    self.page += 1
                    self.pages.append(myPage)
                except Exception, e:
                    print "无法连接糗事百科！", e.message
                    self.enable = False
            else:
                time.sleep(1)

    def ShowPage(self, currentPage, page):
        print u'第%d页\n--------------------------' %page

        for item in currentPage:
            print item

            myInput = raw_input()

            if myInput == 'quit':
                self.enable = False
                break

    def Start(self):
        self.enable = True
        page = self.page

        print u'正在加载中请稍后……'

        thread.start_new_thread(self.LoadPage, ())

        while self.enable:
            if self.pages:
                currentPage = self.pages[0]

                del self.pages[0]

                self.ShowPage(currentPage, page)

                page += 1


print u"""
---------------------------------------
   程序：糗百爬虫
   操作：输入quit退出阅读糗事百科
   功能：按下回车依次浏览今日的糗百热点
---------------------------------------
"""

print u'请按下回车浏览今天的糗百内容：'
raw_input(' ')
myModel = Spider_Model()
myModel.Start()
