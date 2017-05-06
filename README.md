## 描述
根据给定的词条名，进行爬取。保存词条页面，抽取infobox内容存入mongodb中 
 
## 文件说明
BaiduBaieCrawl  
|--BaiduBaike　  存放scrapy代码  
|--data　　存放指定词条data  
|--pagebody　存放词条页面  
|--FailUrl　存放爬取失败页面  
|--Main.py 程序入口  
  
## 使用方法  
将要词条名文件放在文件夹data里，并词条名保存为如下形式:  

阿杜  
阿朵  
阿里郎  
阿木  
阿丘  
阿桑  

一个词条占一行  
```Shell
python　Main.py -t -d  
-t:The name of task   
-d:The name of data which in data folder  
```
for example:
```Shell
python Main.py test test.dat
```
