# -*- coding: utf-8 -*-
import os
import scrapy.cmdline
import sys
from globalValue import *

if __name__=='__main__':

    if len(sys.argv)!=3:
        print 'Usage:python task_name input_name'
        exit(1)

    set_task_name(sys.argv[1])
    set_input_name(sys.argv[2])

    os.chdir('BaiduBaike')
    os.chdir('BaiduBaike')
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'baidubaike'])