#　百度百科爬虫
## 背景
根据给定的词条名，进行爬取。保存词条页面，抽取infobox内容存入mongodb中

## 文件说明
BaiduBaieCrawl
|--BaiduBaike　  存放scrapy代码
|--data　　存放指定词条data
|--pagebody　存放词条页面
|--FailUrl　存放爬取失败页面
|--Main.py 程序入口
|--HandleData.py　预处理程序，单独运行

## 用法
将要爬取的词条名放在文件夹data里，并词条名保存为如下形式：

阿杜
阿朵
阿里郎
阿木
阿丘
阿桑
...

一个词条占一行

commond：python　Main.py task_name data_name.dat

data_name.dat不加路径
