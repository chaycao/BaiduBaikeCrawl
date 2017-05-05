#!/usr/bin/python2
# -*- coding: utf-8 -*-
import scrapy
import urllib
import os
import re
import pymongo
from globalValue import *

class baidubaike(scrapy.Spider):
    name = "baidubaike"
    allowed_domains = ["baike.baidu.com"]

    def __init__(self):
        # 按行读取输入文件，每一行为一个词条名
        # 把词条名加在百度百科主页的URL后面，通过'&'分割
        # 把新的URL加入到start_urls中

        self.start_urls = []
        parDir = os.path.abspath("..")
        mathchObj = re.match('/.*/', parDir)
        dir = mathchObj.group()
        inputPath = dir + 'data/' + get_input_name()
        inputFile = open(inputPath, 'r')
        print ("read file...")
        while 1:
            line = inputFile.readline()
            if not line:
                break;
            self.start_urls.append("http://baike.baidu.com" + "&" + urllib.quote(line))

    def parse(self, response):

        if response.status == 200:
            # 将成功访问的页面放在pagebody文件夹下的task_name文件夹下
            # 页面以URL作为文件名，URL中的'/'符号，替换成'-'
            # 把页面中的infobox内容，进行抽取
            # 抽取后的内容，加上词条名(item_name)，词条URL(itemurl)存到mongodb中
            # mongodb，数据库名:baidubaike，集合名:task_name

            parDir = os.path.abspath("..")
            mathchObj = re.match('/.*/', parDir)
            dir = mathchObj.group()
            dir += "pagebody/" + get_task_name() + '/'
            if not os.path.exists(dir):
                os.mkdir(dir)

            title = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()  # 抽取词条名

            # 词条名不存在，则认为页面爬取失败
            # 将失败的URL保存到FailUrl下，task_name文件中
            if(len(title) == 0):
                dir = mathchObj.group()
                dir += "FailUrl/"
                fileName = get_task_name()
                file = open(dir + fileName, 'a')
                file.write(response.url + "\n")
                return

            # URL作文件名, 斜杠'/'换成'-'
            fileName = response.url.replace('/', '-') + ".html"

            file = open(dir + fileName, 'w')
            file.write(response.body)

            # 保存到mongodb
            con = pymongo.MongoClient('127.0.0.1', 27017)
            db = con['baidubaike']
            collection = db[get_task_name()]
            dict = {}

            # 正则匹配，infobox中的name和value
            pattern = re.compile(r"dt.*?basicInfo-item name\">(.*?)</dt>.*?dd.*?"
                                 r"basicInfo-item value.*?>(.*?)</dd>")
            item = re.findall(pattern, response.body.replace('\n', ' '))

            for i in item:
                itemName = i[0]
                itemValue = i[1]
                # 对可展开的属性，进行特别处理，将多余的部分去除
                p_over = re.compile(r"basicInfo-block overlap\">(.*?)收起")
                s = re.findall(p_over, itemValue)
                if len(s):
                    pattern = re.compile(r"dt.*?basicInfo-item name\">(.*?)</dt>.*?dd.*?basicInfo-item value.*?>"
                                         r"(.*?)<a class=\"toggle toCollapse")
                    x = re.findall(pattern, s[0])
                    itemName = x[0][0]
                    itemValue = x[0][1]

                # 去除多余标签，rule中定义需要去除的标签
                rule = [
                    "<a.*?>",
                    "</a>",
                    "</br>",
                    "<br>",
                    "<em.*?>",
                    "<sup>.*?</sup>"
                ]
                for r in rule:
                    p = re.compile(r)
                    value = re.findall(p, itemValue)
                    for v in value:
                        itemValue = itemValue.replace(v, '')
                    name = re.findall(p, itemName)
                    for n in name:
                        itemName = itemName.replace(n, '')

                # 针对字符实体进行替换
                dict_char = {
                    '&nbsp;' : '', # 空格
                    '&lt;' : '<' , # 小于号
                    '&gt;' : '>' , # 大于号
                    '&amp;' : '&' , # 与
                    '&quot;' : '"'   # 双引号
                }
                for c in dict_char:
                    itemName = itemName.replace(c, dict_char[c])
                    itemValue = itemValue.replace(c, dict_char[c])

                itemName = itemName.strip()
                itemValue = itemValue.strip()

                dict[itemName] = itemValue

            dict['itemurl'] = response.url
            collection.insert(dict)

        else:
            # 返回状态不为200，则认为页面爬取失败
            # 将失败的URL保存到FailUrl下，task_name文件中
            parDir = os.path.abspath("..")
            mathchObj = re.match('/.*/', parDir)
            dir = mathchObj.group()
            dir += "FailUrl/"
            fileName = get_task_name()
            file = open(dir + fileName, 'a')
            file.write(response.url)
