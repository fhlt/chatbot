# /usr/bin/python
# coding:utf-8
# -*- coding:utf-8 -*-

# 输入聊天------图灵机器人回复转换并播放
import log
import time
import sys
import os
import json
import urllib, urllib2
import time
import bosonNLP
import cv2fn
from voiceUtils import VoiceUtils
from tts_xf import text2Voice
from imp import reload
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

reload(sys)  #重新加载sys
sys.setdefaultencoding('utf-8') 

LOC = '重庆市'
API_KEY_YM = '14868ca90be54f58b8a94223f438b3da'
#API_KEY_XL = '4822f3c122d5464e8aee6e0cd03cd094'
raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY_YM

voice_utils = VoiceUtils()

def nowtime():
    return time.strftime('%Y-%m-%d %H:%M:%S ')

class Chat(object):
    key = API_KEY_YM
    apiurl = "http://www.tuling123.com/openapi/api?"  # turing123网站

    def __init__(self):
        os.system("clear")
        print("尽情调教我把!")
        print("------------")
        voice_utils.play_wav('./sound/hello.wav') 

    def get(self):
#        info = input("我:")
        #time.sleep(5)
        info = voice_utils.get_effective_text()
        if info == 'q' or info == 'exit' or info == "quit":
            print("good bye!")
            return
        log.run_log('我：'+info.encode('utf-8'))
        return info
        #self.send(info)
     
    def deleteFile(self, filename):
        if os.path.exists(filename):
            # 删除文件，可使用以下两种方法。
            os.remove(filename)
            # os.unlink(my_file)
        else:
            print('no such file:%s' % filename)

    def send(self, info):
        '''
	if helloWorld(info):
            voice_utils.play_wav('./sound/face_recognition.wav')
            name = cv2fn.get_name_from_cam()
            if name == 'Stranger':
                reply = '您好，但是我好想还不认识您，请您进行人脸注册。'
            else:
                reply = '您好'+name.encode('utf-8')
            text2Voice(reply, './sound/output.wav')
            voice_utils.play_wav('./sound/output.wav')
        else:
        '''
        url = self.apiurl + 'key=' + self.key + '&' +'info='+info + '&loc='+LOC
        print url
        url.encode('utf-8')
        req = urllib2.Request(url.encode(encoding='utf-8'))
        res = urllib2.urlopen(req)
        respose = res.read()
        data = json.loads(respose, encoding='utf-8')
        return data
        '''
        if data['code'] == 100000:           # 回复成功
            res = data['text'].encode('utf-8')               # 回复内容
            #print res
            log.run_log(res)
#            bdr.getVoice(data['text'], "out.wav")  # www.baidu.com
            text2Voice(res, './sound/output.wav')  # www.xfyun.com
            voice_utils.play_wav("./sound/output.wav")
            print "一次播放结束"
        '''
        #self.get()

#api_key = "OodTQR2ESGIGLxxiTBUt4GC6"
#api_secert = "04ONDFc9lDmc1QSi39C3dinqvG13ZGDS"
# 初始化
#bdr = voicedemo.BaiduRest("test_python", api_key, api_secert)
#r = recorder.recoder()                 # 实例化recoder
if __name__ == '__main__':
    chat = Chat()
    chat.get()

