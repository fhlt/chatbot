#!/usr/bin/env python
# coding:utf-8
# -*- coding:utf-8 -*-

from apiFace import baidu_face
import json
# 定义常量
APP_ID = '10588961'
API_KEY = 'vsZrvwSrKtfGYQ0RhI6zD2dV'
SECRET_KEY = 'ZDqoefTSgz1rBzZW06TN6I0w59f0sEdz'

class Face_baidu(object):
    # 初始化baidu_face对象
    aipFace = baidu_face()

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def detect_face_num(self, filePath):
        #image = self.get_file_content(filePath)
	image = filePath
        result = self.aipFace.detect(image=image)
        return result['result_num']

    def enroll_face(self, filePath, uid, userInfo, groupId='group1'):
        #image = self.get_file_content(filePath)
	image = filePath
        result = self.aipFace.addUser(uid=uid,user_info= userInfo, group_id=groupId, image=image)
        if result.__len__() == 1:
            print userInfo+'注册成功:', result['log_id']
            return True
        else:
            print '注册失败'
            print '失败原因：', result['error_msg']
            return False
    
    def delete_user(self, uid):
        result = self.aipFace.deleteUser(uid=uid)
        if result.__len__() == 1:
            print '删除成功', uid
            return True
        else:
            print '删除失败'
            print '失败原因：', result['error_msg']
            return False
            
    def identify_face(self, filePath, groupId='group1'):
        #image = self.get_file_content(filePath)
	image = filePath
        """ 如果有可选参数 """
        options = {}
        options["user_top_num"] = 1
        result = self.aipFace.identifyUser(groupId, image, options)
        scores = 0.1
        name = 'stranger'
        if 'result' in result.keys():
            scores = float(result['result'][0]['scores'][0])
            name = result['result'][0]['user_info']
        return scores, name

    def get_users(self, groupId='group1'):
        result = self.aipFace.getGroupUsers(group_id=groupId)
        return result['result'], result['result_num']

if __name__ == '__main__':
    face = Face_baidu()
    face.get_users()
    #faceNum = face.detect_face_num(filePath='./picture/pic1.jpg')
    #print(faceNum)
    #scores, name = face.identify_face(filePath='./picture/hxy.jpg')
    #if scores > 70:
    #    print 'success', name
    #face.enroll_face(filePath='./picture/hxy.jpg', uid='hls', userInfo='黄老师')

