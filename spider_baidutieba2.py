# -*- coding: utf-8 -*-

import string
import re
import urllib2

class HTML_Tool:
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    EndCharToNoneRex = re.compile("<.*?>")
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    replaceTab = [("<","<"), (">", ">"), ("&", "&"), ("\"", "\""), (" ", " ")]

    def ReplaceChar(self, x):
        x = self.BgnCharToNoneRex.sub("", x)
        x = self.BgnPartRex.sub("\n    ", x)
        x = self.CharToNewLineRex.sub("\n", x)
        x = self.CharToNextTabRex.sub("\t", x)
        x = self.EndCharToNoneRex.sub("", x)

        for t in self.replaceTab:
            x = x.replace(t[0], t[1])

        return x


class BaiduSpider:
    def __init__(self, url):
        self.myUrl = url + '?see_lz=1'
        self.data = []
        self.myTool = HTML_Tool()
        print u'已经启动百度贴吧爬虫'

    def baidu_tieba(self):
        myPage = urllib2.urlopen(self.myUrl).read().decode("utf-8")
        endPage = self.page_counter(myPage)

        title = self.find_title(myPage)

        print u'文章名称：' + title

        self.save_data(self.myUrl, title, endPage)

    def page_counter(self, myPage):
        #匹配“共有<span class="red">12<span>页”来获取总页数
        myMatch = re.search(r'class="red">(\d+?)</span>', myPage, re.S)

        if myMatch:
            endPage = int(myMatch.group(1))
            print u'爬虫报告：发现楼主共有%d页的发布内容。' % endPage
        else:
            endPage = 0
            print u'爬虫报告：无法计算楼主发布内容的页数！'

        return endPage

    def find_title(self, myPage):
        # 匹配<h1 class="core_title_txt" title="">xxxx</h1>找出标题
        myMatch = re.search(r'<h3.*?class="core_title_txt.*?>(.*?)</h3>', myPage, re.S)
        title = u'暂无标题'
        if myMatch:
            title = myMatch.group(1)
        else:
            print u'爬虫报告：无法加载文章标题！'
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')

        return title

    def save_data(self, url, title, endPage):
        self.get_data(url, endPage)
        f = open(title+'.txt', 'w+')
        f.writelines(self.data)
        f.close()
        print u'爬虫报告：文件下载到本地并打包成txt文件！'
        print u'请按任意键退出……'
        raw_input()

    def get_data(self, url, endPage):
        url = url + '&pn='
        for i in range(1, endPage+1):
            print u'爬虫报告：爬虫%d号正在加载中……' % i
            myPage = urllib2.urlopen(url + str(i)).read()

            self.deal_data(myPage.decode('utf-8'))

    def deal_data(self, myPage):
        myItems = re.findall('id="post_content.*?>(.*?)</div>', myPage, re.S)

        for item in myItems:
            datum = self.myTool.ReplaceChar(item.replace("\n","").encode('utf-8'))
            self.data.append(datum+'\n')


print u"""#---------------------------------------
#   程序：百度贴吧爬虫
#   操作：输入网址后自动只看楼主并保存到本地文件
#   功能：将楼主发布的内容打包txt存储到本地。
#---------------------------------------
"""

# 以某小说贴吧为例子
# bdurl = 'http://tieba.baidu.com/p/4321359150?see_lz=1&pn=1'
print u'请输入贴吧的地址最后的数字串：'
bdurl = 'http://tieba.baidu.com/p/' + str(raw_input())

mySpider = BaiduSpider(bdurl)
mySpider.baidu_tieba()
