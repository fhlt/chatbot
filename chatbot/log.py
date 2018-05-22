#!/usr/bin/python
# encoding:utf-8
# -*- coding:utf-8 -*-

import os
import time

RUN = False  # 运行标志
THRESHOLD = 8000  # 声音采集阈值

def nowtime():
    return time.strftime('%Y-%m-%d %H:%M:%S ')


def run_log(text):
    run=open('./run.log', 'a')
    run.write(nowtime()+text+'\n')
    run.close()

if __name__ == '__main__':
    #tex = '证明'
    #run_log('正在注入%s' % tex)
    m = 3
    ud = 'xy'
    for i in range(m):
        uid = ud + str(i)
        print uid
