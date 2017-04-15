# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import urllib

class JavaScriptMiddleware(object):

    def process_request(self, request, spider):

        if spider.name == "baidubaike":

            #　选定浏览器
            driver = webdriver.PhantomJS()

            # 将request.url进行切割获得实体名称
            url = request.url.split('&')[0]
            entity = request.url.split('&')[1]
            entity = urllib.unquote(entity).strip('\n')
            driver.get(url)

            #　加载页面，延迟1s
            time.sleep(1)

            #　给input输入“实体名称”，点击“进入词条”
            js = "document.getElementById(\"query\").value = \"" + entity + "\";\n"+\
                 "document.getElementById(\"search\").click();"

            # 执行js,延迟3s
            driver.execute_script(js)
            time.sleep(5)

            body = driver.page_source
            print entity
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return
