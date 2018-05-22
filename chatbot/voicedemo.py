#!/usr/bin/python
# _*_ coding:UTF-8 _*_
# coding=utf-8


import urllib
import urllib2
import json
import base64
import urlparse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        # token url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        #  resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # voice identification resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.get token
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib2.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        # 2. Rest submit
        get_url = self.getvoice_url % (urllib2.quote(text), self.cu_id, self.token_str)
        print(get_url)
        req = urllib2.Request(get_url.encode(encoding='utf-8'))
        res = urllib2.urlopen(req)
        voice_data = res.read()
        # 3.handle result
        voice_fp = open(filename, 'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def getText(self, filename):
        # 2. submit data
        data = {}
        # some para
        data['format'] = 'wav'
        data['rate'] = 8000              
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename, 'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        req = urllib2.Request(self.upvoice_url, data = bytes(post_data))
        res = urllib2.urlopen(req)
        respose = res.read()
        # 3.return handled data
        r_data = json.loads(respose)
        print r_data
        if r_data['err_msg'] == 'success.':
            return r_data["result"][0]
        else:
            return None

if __name__ == "__main__":
    api_key = "OodTQR2ESGIGLxxiTBUt4GC6"
    api_secert = "04ONDFc9lDmc1QSi39C3dinqvG13ZGDS"
    # init
    bdr = BaiduRest("test_python", api_key, api_secert)

    #bdr.getVoice("您好，请问我该怎么称呼您？", "ask_name.wav")

    print(bdr.getText("./sound/recoder.wav"))

