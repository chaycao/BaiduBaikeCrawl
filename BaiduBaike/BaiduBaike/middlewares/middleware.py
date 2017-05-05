# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import urllib

class JavaScriptMiddleware(object):
    '''通过Selenium调用Phantomjs的下载中间件.

    将请求，利用Phantomjs加载页面，返回js加载后的页面body
    '''

    def process_request(self, request, spider):
        '''Scrapy定义的下载中间件的回调函数

        将请求发给下载中间件，利用Phantomjs加载页面，返回js加载后的页面body

        :param request:发送的请求，可获得请求url，用Phantomjs进行访问
        :param spider:scrapy自带
        :return:Phantomjs加载后的页面body
        '''

        if spider.name == "baidubaike":
            driver = webdriver.PhantomJS()  # 选定浏览器
            url = request.url.split('&')[0]  # 切割获得实体名称
            entity = request.url.split('&')[1]
            entity = urllib.unquote(entity).strip('\n')
            driver.get(url)

            # 加载页面，延迟1s
            time.sleep(1)

            # 给input输入“实体名称”，点击“进入词条”
            js = ("document.getElementById(\"query\").value = \"" + entity + "\";\n"
                  "document.getElementById(\"search\").click();")

            # 执行js,延迟5s
            driver.execute_script(js)
            time.sleep(5)

            body = driver.page_source
            print entity
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return
