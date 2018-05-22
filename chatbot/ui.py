#!/usr/bin/env python
# encoding=utf-8
#-*- coding:utf-8 -*-
'''
Basic Layout
'''
#from __future__ import print_function, unicode_literals
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit, QFrame, QMessageBox
import cv2fn 
import log
from log import RUN
import bosonNLP
import ssl
from jiebaPart import is_quit
from ChatThread import ChatThread
from chatBot import voice_utils
from tts_xf import text2Voice

ssl._create_default_https_context = ssl._create_unverified_context

class chatBotUI(QWidget):
    def __init__(self):
        super(chatBotUI,self).__init__()
       # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
       # self.setStyleSheet('background-color:#F0FFFF')
	self.initUi()
	self.showMaximized()
	#self.showFullScreen()

    def initUi(self):
        self.createLeftUpBox()
        self.createRightBox()
	self.createLeftDownBox()

        self.resultLabel = QLabel('result')
        self.resultLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)        

        mainLayout = QHBoxLayout()
        hboxLayout = QVBoxLayout()

      # 	hboxLayout.addStretch()  
        hboxLayout.addWidget(self.leftUpBox, 1)
        hboxLayout.addWidget(self.leftDownBox, 2)

       	mainLayout.addLayout(hboxLayout, 1)
        mainLayout.addWidget(self.rightBox, 2)
        self.setLayout(mainLayout)

    def createLeftUpBox(self):
        self.leftUpBox = QGroupBox("para")
        layout = QGridLayout()

        mLabel = QLabel("Volume of training")
        self.mLineEdit = QLineEdit("1")
        soundLabel = QLabel("Sound threshlod")
        self.soundLineEdit = QLineEdit("8000")
       	
#        layout.setSpacing(10) 
        layout.addWidget(mLabel,1,0)
        layout.addWidget(self.mLineEdit,1,1)
        layout.addWidget(soundLabel,2,0)
        layout.addWidget(self.soundLineEdit,2,1)
	
   #     layout.setColumnStretch(1, 10)
        self.leftUpBox.setLayout(layout)
        self.setWindowTitle('Basic Layout')

    def createRightBox(self):
        self.rightBox = QGroupBox()
        layout = QVBoxLayout()
 
        self.imgeLabel = QLabel()
	pixMap = QPixmap('./picture/pic1.jpg')
	self.imgeLabel.setPixmap(pixMap)

        self.bigEditor = QTextEdit()
        self.bigEditor.setPlainText("等待操作......")
	self.bigEditor.setReadOnly(True)
        layout.addWidget(self.imgeLabel)
        layout.addWidget(self.bigEditor)
        self.rightBox.setLayout(layout)

    def createLeftDownBox(self):
        self.leftDownBox = QGroupBox("button layout")
        layout = QVBoxLayout()
	self.faceRecButton = QPushButton('face recogniton', self)
	self.faceRecButton.setStyleSheet('QPushButton{background-color:#16A085;bord:none;color:#ffffff;font-size:20px}')
			#	'QPushButton:hover{background-color:#333333;}') 
	self.studyButton = QPushButton('study', self)
        self.getUserButton = QPushButton('usersList', self)

        self.faceRecButton.clicked.connect(self.face_rec)
        self.studyButton.clicked.connect(self.study_finish)
        self.getUserButton.clicked.connect(self.get_user_list)

	self.startButton = QPushButton('start', self)
	self.closeButton = QPushButton('close', self)
	self.setButton = QPushButton('set threshold', self)
        self.startButton.clicked.connect(self.start_chat)
        self.closeButton.clicked.connect(self.close_chat)
        self.setButton.clicked.connect(self.set_sound_threshold)
        self.closeButton.setEnabled(False)

	layout.addWidget(self.faceRecButton, 1)
	layout.addWidget(self.studyButton, 1)
        layout.addWidget(self.getUserButton,1)
	layout.addWidget(self.startButton, 1)
	layout.addWidget(self.closeButton, 1)
	layout.addWidget(self.setButton,1)
        self.leftDownBox.setLayout(layout)
   
    def get_user_list(self):
        self.bigEditor.setText('获取人脸库')
        self.getUserButton.setEnabled(False)
        #log.run_log('正在获取人脸库...')
        information = cv2fn.get_group_users()
        QMessageBox.information(self, '人脸库', information)
        self.getUserButton.setEnabled(True) 

    # 设置声音采集阈值
    def set_sound_threshold(self):
        threshold = self.soundLineEdit.text().strip()  #sound catch threshold
        from log import THRESHOLD
        THRESHOLD = int(threshold)
        self.bigEditor.setText('设置声音采集阈值完成:'+threshold)

    #  face recognition
    def face_rec(self):
        self.bigEditor.setText('开始人脸识别')
        self.faceRecButton.setEnabled(False)
        voice_utils.play_wav('./sound/face_recognition.wav')
        name = cv2fn.get_name_from_cam()
        pixMap = QPixmap('./picture/pic1.jpg')
        self.imgeLabel.setPixmap(pixMap)
        self.bigEditor.setText('人脸识别结束'+name)
        self.faceRecButton.setEnabled(True)
        

    def study_finish(self):
        self.bigEditor.setText('开始学习人脸特征')
        self.studyButton.setEnabled(False)
        m = self.mLineEdit.text().strip()
        m = int(m)
        name = None
        while name == None:
            voice_utils.play_wav('./sound/ask_name.wav')
            #chatBot.r.recoder()
            #chatBot.r.savewav('./sound/user_reply.wav')
            info = voice_utils.get_effective_text()
            name = bosonNLP.bosonNLP_ner(info)
            if is_quit(info):
                # 立即退出人脸学习
                self.studyButton.setEnabled(True)
                return
        #name = name.encode('utf-8')
        name_success = "好的"+name.encode('utf-8')+'。接下来我将会用几秒钟的时间学习您的面部特征，请您站到镜头前指定区域，谢谢配合'
        text2Voice(name_success, './sound/output.wav')
        voice_utils.play_wav('./sound/output.wav') 
        ret = cv2fn.study_person_face(m, name)
        if ret > 0 and ret == m:
            log.run_log('完成全部学习任务!')
        elif ret == 0:
            log.run_log('学习任务未完成:')
        else:
            log.run_log('完成部分学习任务:')
            
	#print('study button clicked')
        QMessageBox.information(self, 'result', '您的面部特征已经学习完成!'+ name.encode('utf-8'))
        self.resultLabel.setText('result')
        self.bigEditor.setText('面部特征学习完成'+name.encode('utf-8'))
        self.studyButton.setEnabled(True)

    # 开始聊天线程
    def start_chat(self):
        self.bigEditor.setText('开始聊天')
        self.startButton.setEnabled(False)
        self.closeButton.setEnabled(True)
        self.chat_thread = ChatThread()
        self.chat_thread._signal.connect(self.update_ui)
        self.chat_thread.start()

    # 更新ui中的照片
    def update_ui(self, signal):
        print type(signal)
        if signal == 1:
            pixMap = QPixmap('./picture/pic1.jpg')
            self.imgeLabel.setPixmap(pixMap)

    
    # 结束聊天线程
    def close_chat(self):
        self.bigEditor.setText('关闭聊天')
        self.chat_thread.terminate()
        self.startButton.setEnabled(True)
        self.closeButton.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = chatBotUI()
    ex.show()
    sys.exit(app.exec_())
