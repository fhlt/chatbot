#!/usr/bin/python
# encoding=utf8
# -*- coding: UTF-8 -*-

import jieba
import jieba.analyse
import jieba.posseg
import numpy as np

CQUT_keyWords = ['理工大学', '重庆', '官网', '打开']

# 计算余弦相似度
def cos_like(x, y):
    tx = np.array(x)
    ty = np.array(y)
    cos1 = np.sum(tx*ty)
    cos21 = np.sqrt(sum(tx**2))
    cos22 = np.sqrt(sum(ty**2))
    return cos1/float(cos21*cos22)

def predict_next(text):
    next = 0
    s_list = []
    seg_list = jieba.analyse.extract_tags(text, 5)
    for s in seg_list:
        s_list.append(s.encode('utf-8'))
    if helloWorld(s_list):
        next = 1      # 启动人脸识别
    else:
        cosimi = caculate_cosimi(CQUT_keyWords, s_list)
        if cosimi > 0.7:  # 以0.7作为分界
            next =  2     # 重庆理工大学官网
    return next
        
    

def caculate_cosimi(keyWords, seg):
    vocabSet = set(keyWords)
    vocabSet = vocabSet | set(seg)
    vocabSet = list(vocabSet)   # create VocabList
    tx = [0]*len(vocabSet)
    ty = [0]*len(vocabSet)
    for word in vocabSet:
        if word in keyWords:
            tx[vocabSet.index(word)] = 1
        if word in seg:
            ty[vocabSet.index(word)] = 1
    cosimi = cos_like(tx, ty)  # 计算余弦相似度
    return cosimi

def helloWorld(seg_list):
    str1 = '小龙';flag1 = 0
    str2 = '你好';flag2 = 0
    str3 = '您好';flag3 = 0
    hello = False
    for tmp in seg_list:
        if tmp == str1:
            flag1 = 1
        elif tmp == str2:
            flag2 = 1
        elif tmp == str3:
            flag3 = 1
    if flag1 == 1 and (flag2 == 1 or flag3 ==1):
        hello = True
    return hello


def is_quit(text):
    str1 = '退出'
    str2 = '停止'
    str3 = '结束'
    str4 = 'stop'
    quit = False
    sef_list = jieba.analyse.extract_tags(text, 3)
    for s in sef_list:
        tmp = s.encode('utf-8')
        if tmp == str1 or tmp == str2 or tmp == str3 or tmp == str4:
            quit = True
            break
    return quit


if __name__ == '__main__':
    sentence = '理工大学官网'
    cqut(sentence)
    #seg_list = jieba.posseg.cut(sentence)
    #for s in seg_list:
    #    print s
