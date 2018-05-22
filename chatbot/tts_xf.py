# !usr/bin/python
# encoding=utf8
# -*- coding: UTF-8 -*-

import base64
import json
import time
import hashlib
import urllib, urllib2


# 使用科大讯飞的文本转语音服务
def text2Voice(text, filename):
    # API请求地址、API KEY、APP ID等参数
    api_url = "http://api.xfyun.cn/v1/service/v1/tts"
    API_KEY = "4946e92f565fc2f11fd1b52dc1706e89"
    APP_ID = "5ae87397"
#    OUTPUT_FILE = "./output.wav"    # 输出音频的保存

    # 构造输出音频配置参数
    Param = {
        "auf": "audio/L16;rate=16000",    #音频采样率
        "aue": "raw",    #音频编码，raw(生成wav)或lame(生成mp3)
        "voice_name": "xiaoyan",
        "speed": "50",    #语速[0,100]
        "volume": "77",    #音量[0,100]
        "pitch": "50",    #音高[0,100]
        "engine_type": "aisound"    #引擎类型。aisound（普通效果），intp65（中文），intp65_en（英文）
    }
    # 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
    Param_str = json.dumps(Param)    #得到明文字符串
    Param_utf8 = Param_str.encode('utf8')    #得到utf8编码(bytes类型)
    Param_b64 = base64.b64encode(Param_utf8)    #得到base64编码(bytes类型)
    Param_b64str = Param_b64.decode('utf8')    #得到base64字符串

    # 构造HTTP请求的头部
    time_now = str(int(time.time()))
    checksum = (API_KEY + time_now + Param_b64str).encode('utf8')
    checksum_md5 = hashlib.md5(checksum).hexdigest()
    header = {
        "X-Appid": APP_ID,
        "X-CurTime": time_now,
        "X-Param": Param_b64str,
        "X-CheckSum": checksum_md5
    }
    # 手工输入需要将该句删掉
    #text = text.encode('utf-8')
    # 构造HTTP请求Body
    body = {
        "text": text
    }
    body_urlencode = urllib.urlencode(body)
    body_utf8 = body_urlencode.encode('utf8')

    # 发送HTTP POST请求
    req = urllib2.Request(api_url, data=body_utf8, headers=header)
    response = urllib2.urlopen(req)

    # 读取结果
    response_head = response.headers['Content-Type']
    if(response_head == "audio/mpeg"):
        out_file = open(filename, 'wb')
        data = response.read()  # a 'bytes' object
        out_file.write(data)
        out_file.close()
        print('输出文件: ' + filename)
    else:
	print('未认证的IP')
        print(response.read().decode('utf8'))


if __name__ == '__main__':
    text2Voice('正在为您打开重庆理工大学官网。','./sound/cqut.wav')
