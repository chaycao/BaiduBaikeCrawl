# -*- coding: utf-8 -*-

'''声明全局变量,task_name,input_name.任务名，输入文件名

各文件中通过set，get设置和获取

'''

def set_task_name(name):
    global task_name
    task_name = name

def get_task_name():

    return task_name

def set_input_name(name):
    global input_name
    input_name = name

def get_input_name():

    return input_name
