# -*- coding: utf-8 -*-

import pymongo
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

if __name__=='__main__':
    str = '演员，制片人，导演'
    arrs = re.split('，',str)
    for arr in arrs :
        print arr