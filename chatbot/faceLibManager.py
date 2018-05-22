#!/usr/bin/python
# encoding=utf-8
# -*- coding=utf-8 -*-
faceLib = './faceLib/face_lib.db'

def add_user(uid,name):
    fp = open(faceLib,'a+')
    arrayOfLines = fp.readlines()
    no = len(arrayOfLines) + 1
    tmpStr = ''.join(name+'\t'+uid+'\n')
    fp.write(tmpStr)
    fp.close()

if __name__ == '__main__':
    add_user('zhangdong','张东')
