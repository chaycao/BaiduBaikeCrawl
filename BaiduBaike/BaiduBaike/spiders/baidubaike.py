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

    # 初始化start_urls，以及把实体名称保存在一个list中
    def __init__(self):
        self.start_urls = []

        parDir = os.path.abspath("..")
        mathchObj = re.match('/.*/', parDir)
        dir = mathchObj.group()

        inputPath = dir + 'data/' + get_input_name()
        inputFile = open(inputPath, 'r')
        print ("读取实体名称，生成url")

        while 1:
            line = inputFile.readline()
            if not line:
                break;
            self.start_urls.append("http://baike.baidu.com" + "&" + urllib.quote(line))


    def parse(self, response):

        if response.status == 200:
            #　获取BaiduBaikeCrawl文件夹的目录
            parDir = os.path.abspath("..")
            mathchObj = re.match('/.*/', parDir)
            dir = mathchObj.group()

            # 保存到pagebody文件夹中，文件名取实体名称
            dir += "pagebody/"
            title = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()
            if(len(title) == 0):
                # 把失败的url进行保存
                dir = mathchObj.group()
                # 保存到pagebody文件夹中，文件名取实体名称
                dir += "FailUrl/"
                fileName = get_task_name()
                file = open(dir + fileName, 'a')
                file.write(response.url+"\n")
                return

            fileName = title[0] + ".html"
            file = open(dir + fileName,'w')
            file.write(response.body)

            # 将infobox中的信息保存到mongodb中，集合名为当天日期
            con = pymongo.MongoClient('127.0.0.1', 27017)
            db = con['baidubaike']
            collection = db[get_task_name()]
            dict = {}

            # 正则匹配，infobox中的name和value
            pattern = re.compile(r"dt.*?basicInfo-item name\">(.*?)</dt>.*?dd.*?basicInfo-item value.*?>(.*?)</dd>")
            item = re.findall(pattern, response.body.replace('\n', ' '))

            for i in item:
                itemName = i[0].replace("&nbsp;","")
                itemValue = i[1].replace("&nbsp;","")

                #针对可以展开的属性,将多余的部分去除
                p_over = re.compile(r"basicInfo-block overlap\">(.*?)收起")
                s = re.findall(p_over,itemValue)
                if len(s):
                    pattern = re.compile(r"dt.*?basicInfo-item name\">(.*?)</dt>.*?dd.*?basicInfo-item value.*?>(.*?)<a class=\"toggle toCollapse")
                    x = re.findall(pattern,s[0])
                    itemName = x[0][0].replace("&nbsp;","")
                    itemValue = x[0][1].replace("&nbsp;","")

                # 匹配rule，去除多余标签
                rule =[
                    "<a.*?>",
                    "</a>",
                    "</br>",
                    "<br>",
                    "<em.*?>"
                ]
                for r in rule:
                    p = re.compile(r)
                    value = re.findall(p, itemValue)
                    for v in value:
                        itemValue = itemValue.replace(v, '')
                itemName = itemName.strip()
                itemValue = itemValue.strip()

                dict[itemName] = itemValue

            dict['itemurl'] = response.url
            collection.insert(dict)

        else:
            # 把失败的url进行保存
            parDir = os.path.abspath("..")
            mathchObj = re.match('/.*/', parDir)
            dir = mathchObj.group()

            # 保存到pagebody文件夹中，文件名取实体名称
            dir += "FailUrl/"
            fileName = get_task_name()
            file = open(dir + fileName, 'a')
            file.write(response.url)

            #collection.insert(dict)
