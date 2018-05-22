#!/usr/bin/python
# encoding=utf8
# -*- coding: UTF-8 -*-
import base64
import json
import urllib
import urllib2
# 定义常量
APP_ID = '10588961'
API_KEY = 'vsZrvwSrKtfGYQ0RhI6zD2dV'
SECRET_KEY = 'ZDqoefTSgz1rBzZW06TN6I0w59f0sEdz'


class baidu_face():
    """
            人脸识别
    """
    '''
    def __init__(self):
        request_url = self.__accessTokenUrl + '?grant_type=client_credentials' + '&client_id=' + API_KEY \
              + '&client_secret=' + SECRET_KEY
        request = urllib2.Request(url=request_url)
        request.add_header('Content-tyep', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        self.access_token = data['access_token']
   '''
    access_token = '24.6e4b6ffb0617543192498caf8135a0ce.2592000.1528342483.282335-10588961'

    __accessTokenUrl = 'https://aip.baidubce.com/oauth/2.0/token'

    __detectUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/detect'

    __matchUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/match'

    __identifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/identify'

    __verifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/verify'

    __multiIdentifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/multi-identify'

    __userAddUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/add'

    __userUpdateUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/update'

    __userDeleteUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/delete'

    __userGetUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/get'

    __groupGetlistUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/getlist'

    __groupGetusersUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/getusers'

    __groupAdduserUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/adduser'

    __groupDeleteuserUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/group/deleteuser'

    __personVerifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/person/verify'

    __faceverifyUrl = 'https://aip.baidubce.com/rest/2.0/face/v2/faceverify'

    def detect(self, image, options=None):
        '''
            人脸检测
        :param image:
        :param options:
        :return:
        '''
        # 二进制方式打开图片文件
        f = open(image, 'rb')
        img = base64.b64encode(f.read())

        params = {
             "face_fields": "age,gender,glasses,race,qualities",
             "image": img,
             "max_face_num": 5
            }
        params = urllib.urlencode(params)
        request_url = self.__detectUrl + "?access_token=" + self.access_token
        request = urllib2.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
	result = json.loads(content, encoding='utf-8')
        return result

    def addUser(self, uid, user_info, group_id, image, options=None):
        '''
            人脸注册
        :param uid:
        :param user_info:
        :param group_id:
        :param image:
        :param options:
        :return:
        '''
        # 以二进制方式打开文件
        f = open(image, 'rb')
        # 参数images：图像base64编码
        img = base64.b64encode(f.read())

        params = {
            "group_id": group_id,
            "images": img,
            "uid": uid,
            "user_info": user_info}
        params = urllib.urlencode(params)

        request_url = self.__userAddUrl + "?access_token=" + self.access_token
        request = urllib2.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
	result = json.loads(content, encoding='utf-8')
        return result

    def deleteUser(self, uid, options=None):
        '''
           删除用户
        '''
        params = {'uid':uid}
        params = urllib.urlencode(params)
        request_url = self.__userDeleteUrl + '?access_token=' + self.access_token
        request = urllib2.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
        result = json.loads(content, encoding='utf-8')
        return result

    def getGroupUsers(self, group_id, options=None):
        '''
            组内用户列表查询
        '''
        params = {"end": 100,"group_id": group_id,"start": 0}
        params = urllib.urlencode(params)
        request_url = self.__groupGetusersUrl + '?access_token=' + self.access_token
        request = urllib2.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
        result = json.loads(content, encoding='utf-8')
        return result

    def identifyUser(self, group_id, image, options=None):
        '''
            人脸查找
        :param group_id:
        :param image:
        :param options:
        :return:
        '''
        # 以二进制方式打开文件
        f = open(image, 'rb')
        # 参数images：图像base64编码
        img = base64.b64encode(f.read())

        params = {
            "face_top_num": "1",
            "group_id": group_id,
            "images": img,
            "user_top_num": "1"}
        params = urllib.urlencode(params)

        request_url = self.__identifyUrl + "?access_token=" + self.access_token
        request = urllib2.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
	result = json.loads(content, encoding='utf-8')
        return result


if __name__ == '__main__':
    baiduface = baidu_face()
    #result = baiduface.identifyUser(group_id='group1', image='./picture/pic1.jpg')
    #print(result)
    #result = baiduface.addUser('hxy','黄老师', 'group1', './picture/hxy.jpg')
    result = baiduface.deleteUser(uid='user1')
    print(result)

