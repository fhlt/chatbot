#!/usr/bin/python
# encoding=utf-8
# -*- coding=utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal
from chatBot import Chat
from jiebaPart import predict_next
from chatBot import voice_utils
from tts_xf import text2Voice
import cv2fn
import log
import webbrowser

class ChatThread(QThread):
    # 定义信号用于更新ui
    _signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ChatThread, self).__init__(parent)
        

    def run(self):
        chat = Chat()
        while True:
            info = chat.get()
            next = predict_next(info)
            if next == 1:
                # 激活人脸识别 
                voice_utils.play_wav('./sound/face_recognition.wav')
                name = cv2fn.get_name_from_cam()
                self._signal.emit(1)      # 更新ui图片
                print '更新ui'
                if name == 'Stranger':
                    reply = '您好，但是我好想还不认识您，请您进行人脸注册。'
                else:
                    reply = '您好'+name.encode('utf-8')
                text2Voice(reply, './sound/output.wav')
                voice_utils.play_wav('./sound/output.wav')
            elif next == 2:
                # 打开重理工官网
                url = 'http://www.cqut.edu.cn'
                webbrowser.open_new_tab(url)
                voice_utils.play_wav('./sound/cqut.wav')
            else:
                data = chat.send(info)
                if data['code'] == 100000:          # 文本
                    res = data['text'].encode('utf-8')
                    print res
                    log.run_log(res)
                    text2Voice(res, './sound/output.wav')
                    voice_utils.play_wav('./sound/output.wav')
                elif data['code'] == 200000:       # 链接
                    url = data['url']
                    text2Voice(data['text'].encode('utf-8'),'./sound/output.wav')
                    webbrowser.open_new_tab(url)
                    voice_utils.play_wav('./sound/output.wav')
                elif data['code'] == 302000:     # 新闻
                    url = data['list'][0]['detailurl']
                    webbrowser.open_new_tab(url)
                    voice_utils.play_wav('./sound/news.wav')
                elif data['code'] == 308000:     # 菜谱
                    url = data['list'][0]['detailurl']
                    webbrowser.open_new_tab(url)
                    voice_utils.play_wav('./sound/cookbook.wav')


