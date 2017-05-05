# -*- coding: utf-8 -*-
import os
import pymongo
import re


def TravelFile(path):
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
            iter_f = iter(f)
            str = ""
            for line in iter_f:
                str = str + line
            pagebody = str

def Extract(pagebody):
    # 将infobox中的信息保存到mongodb中，集合名为当天日期
    con = pymongo.MongoClient('127.0.0.1', 27017)
    db = con['pagebody']
    collection = db['test01']
    dict = {}

    # 正则匹配，infobox中的name和value
    pattern = re.compile(r"dt.*?basicInfo-item name\">(.*?)</dt>.*?dd.*?basicInfo-item value.*?>(.*?)</dd>")
    item = re.findall(pattern, pagebody.replace('\n', ' '))

    for i in item:
        itemName = i[0].replace("&nbsp;", "")
        itemValue = i[1].replace("&nbsp;", "")

        # 针对可以展开的属性,将多余的部分去除
        p_over = re.compile(r"basicInfo-block overlap\">(.*?)收起")
        s = re.findall(p_over, itemValue)
        if len(s):
            pattern = re.compile(
                r"dt.*?basicInfo-item name\">(.*?)</dt>.*?dd.*?basicInfo-item value.*?>(.*?)<a class=\"toggle toCollapse")
            x = re.findall(pattern, s[0])
            itemName = x[0][0].replace("&nbsp;", "")
            itemValue = x[0][1].replace("&nbsp;", "")

        # 匹配rule，去除多余标签
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
                if(r == "<br>"):
                    itemValue = itemValue.replace(v, ';')
                    continue
                itemValue = itemValue.replace(v, '')
        itemName = itemName.strip()
        itemValue = itemValue.strip()

        dict[itemName] = itemValue

        dict['itemurl'] = response.url
    collection.insert(dict)