#!/usr/bin/python
# encoding=utf8
# -*- coding: UTF-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests


NER_URL = 'http://api.bosonnlp.com/ner/analysis'
KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'

BOSON_API_KEY = 'vdlz4hos.25477.obsWY3ICw0OY'

# 命名实体识别
def bosonNLP_ner(s):
    data = json.dumps(s)
    headers = {'X-Token': BOSON_API_KEY}
    resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))
    name = None
    for item in resp.json():
        for entity in item['entity']:
            if entity[2] == 'person_name':
                name = ''.join(item['word'][entity[0]])
                break
            #print(''.join(item['word'][entity[0]:entity[1]]), entity[2])
        if name:
            break
    return name

# 在线分词-关键字 
def bosonNLP_keywords(text):
    params = {'top_k': 3}
    data = json.dumps(text)
    headers = {'X-Token': BOSON_API_KEY}
    resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))
    for weight, word in resp.json():
        print(weight, word)


if __name__ == '__main__':
    #bosonNLP_keywords(text='小龙你好...')
    name = bosonNLP_ner(s='你吃饭了吗')
    print(name)
