# /usr/bin/python
# coding:utf-8
# -*- coding:utf-8 -*-
import face
import cv2
import os
from xpinyin import Pinyin
import pickle
import log
import face_recognition
from faceLibManager import add_user

#faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
p = Pinyin()
tmpDir = 'tmp'
if not os.path.exists(tmpDir):
    os.mkdir(tmpDir)
# 摄像头

face = face.Face_baidu()

# 人脸检测部分
def detect_face(img):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    faces = face_recognition.face_locations(img)
    return faces

def delete_user_face(uid):
    result = face.delete_user(uid)
    if result:
        log.run_log('删除成功：'+uid)  # uid是西文字符
        updown_users_lib()
    else:
        log.run_log('删除失败：'+uid)
    return result

def study_person_face(m, name):
    picPath = auto_take_picture(m)
    ud = p.get_pinyin(name)
    result = 0
    for i in range(m):
        # 数字字母下划线构成
        uid = ud + str(i)
        uid = uid.replace('-', '_')
        ret = face.enroll_face(filePath=picPath[i], uid=uid, userInfo=name.encode('utf-8'))
        if ret == False:
            # 注册成员
            add_user(uid.encode('utf-8'), name.encode('utf-8'))
            log.run_log('注册失败：%s' % name.encode('utf-8'))
        else:
            log.run_log('注册成功：%s' % name.encode('utf-8'))
            result = result + 1
    return result

def get_group_users(faceLibDir='./faceLib/face_lib.db'):
    if not os.path.exists(faceLibDir):
        return None
    fp = open(faceLibDir)
    arrayOfLines = fp.readlines()
    numberOfLines = len(arrayOfLines)
    returnStr = 'id\t'+'name\t'+'uid\n'
    i = 1
    for line in arrayOfLines:
        line = line.strip()
        listFormLine = line.split('\t')
        tmpStr = '%d\t' % i + listFormLine[0] + '\t' + listFormLine[1] + '\n'
        returnStr = returnStr + tmpStr
        i = i + 1
    return returnStr
        

# 获取组内用户信息,和服务器同步数据
def updown_users_lib(faceLibDir='./faceLib/face_lib.db'):
    result, m = face.get_users()
    #if not os.path.exists(faceLibDir)
    #    os.mkdir(faceLibDir)
    fp = open(faceLibDir, 'w')
    for item in result:
        faceInfo = item['user_info'] + '\t' + item['uid'] + '\n'
        fp.write(faceInfo.encode('utf-8'))
    fp.close()
    return result

# 从摄像头中拍照并进行人物识别
def get_name_from_cam():
    personName ='Stranger'
    picPath = auto_take_picture(1)
    scores, name = face.identify_face(filePath=picPath[0])
    if scores > 70:
        personName = name
        print 'success:', p.get_pinyin(personName)
    img = cv2.imread(picPath[0])
    #faces = detect_face(img)
    fp = open(os.path.join('picture', 'last.ckg'), 'rb')  # rb 表示读取二进制文件
    (top, right, bottom, left) = pickle.load(fp)
    fp.close()
    cv2.rectangle(img, (left, top), (right, bottom), (255,0,0), 2)
    cv2.putText(img, p.get_pinyin(personName), (left, top - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv2.imwrite(picPath[0], img)
    log.run_log('照片存放于./picture,识别结果:')
    return personName


def auto_take_picture(num, storageDir = 'picture'):
    if not os.path.exists(storageDir):
        os.mkdir(storageDir)
    log.run_log('正在尝试学习面部特征...')
    cap = cv2.VideoCapture(0)
    picNum = 1
    if not cap.isOpened():
        log.run_log('摄像头打开失败')
        print 'Cap failed because of camera'
    success, img = cap.read()
    #print 'read success:', success
    #不成功就不停
    while success:
        #print 'success:', success
        success, img = cap.read()
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 图像灰化
        faces = detect_face(img)

        for face in faces:
            top, right, bottom, left = face
            if len(faces) == 1:
                print top, right, bottom, left
                fp = open(os.path.join(storageDir, 'last.ckg'), 'wb')
                pickle.dump((top, right, bottom, left), fp)
                fp.close()
            #img = cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)  # 在人脸区域画一个正方形出来
            '''  
            ROI = gray[x:x + w, y:y + h]
            ROI = cv2.resize(ROI, (128, 128), interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(os.path.join(tmpDir, 'picROI.jpg'), ROI)
            
            scores, name = face.identify_face(os.path.join(tmpDir, 'picROI.jpg'))
            print(name)
            if scores > 70:
                show_name = name
            else:
                show_name = 'Stranger'
            cv2.putText(img, show_name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            '''

        cv2.imshow('Image', img)
        if len(faces) == 1:
            cv2.imwrite(os.path.join(storageDir, 'pic%s.jpg' % picNum), img)
            log.run_log('已将照片存放在picture文件夹下')
            picNum += 1
            print('one face found')
        elif not faces:
            print('No face found')
        else:
            print('More than one face found')
        if picNum > num:
            break
    cap.release()
    cv2.destroyAllWindows()
    return [os.path.join(storageDir, 'pic%s.jpg' % i) for i in range(1, num + 1)]


def manual_take_picture(num, storageDir = 'picture'):
    if not os.path.exists(storageDir):
        os.mkdir(storageDir)
    cap = cv2.VideoCapture(0)
    picNum = 1
    if not cap.isOpened():
        print('Cap failed because of camera')
    print('Press **SPACE** to capture a picture')
    success, img = cap.read()
    while success and cv2.waitKey(1) == -1:
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 图像灰化
        faces = detect_face(img)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 在人脸区域画一个正方形出来
            ROI = gray[x:x + w, y:y + h]
            ROI = cv2.resize(ROI, (128, 128), interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(os.path.join(tmpDir, 'picROI.jpg'), ROI)
            scores, name = face.identify_face(os.path.join(tmpDir, 'picROI.jpg'))
            print(name)
            if scores > 70:
                show_name = name
            else:
                show_name = 'Stranger'
            cv2.putText(img, p.get_pinyin(show_name), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            cv2.imshow('Capture Image', img)
            if len(faces) == 1:
                cv2.imwrite(os.path.join(storageDir, 'pic%s.jpg' % picNum), img)
                picNum += 1
                print('one face found')
            elif not faces:
                print('No face found')
            else:
                print('More than one face found')
            if picNum > num:
                break
    cap.release()
    cv2.destroyAllWindows()
    return [os.path.join(storageDir, 'pic%s.jpg' % i) for i in range(1, num + 1)]


if __name__ == '__main__':
    uid = 'zt'
    userInfo = '张田'
    #updown_users_lib()
    #print get_group_users()
    delete_user_face(uid='zhou0')
    #get_name_from_cam()
    #picPath = auto_take_picture(2)
    '''
    for filePath in picPath:
        print(filePath)
        #face.enroll_face(filePath=filePath, uid=uid, userInfo=userInfo)
    print('学习完成')
    '''
