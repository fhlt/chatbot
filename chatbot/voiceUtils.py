#!/usr/bin/python
# encoding=utf-8
# -*- coding: utf-8 -*-

# voiceUtils
from recorder import recoder
from voicedemo import BaiduRest

recoder_file = './sound/recoder.wav'


class VoiceUtils(object):
    def __init__(self):
        api_key = "OodTQR2ESGIGLxxiTBUt4GC6"
        api_secert = "04ONDFc9lDmc1QSi39C3dinqvG13ZGDS"
        # 初始化
        self.bdr = BaiduRest("test_python", api_key, api_secert)
        self.r = recoder()

    # 向上提供可靠的语音及文本
    def get_effective_text(self):
        self.r.recoder()
        self.r.savewav(recoder_file)
        info = self.bdr.getText(recoder_file)
        # info不能太短
        while info is None or len(info) <= 1:
            self.r.recoder()
            self.r.savewav(recoder_file)
            info = self.bdr.getText(recoder_file)
        return info

    def play_wav(self, filename):
        self.r.playwav(filename)


if __name__ == '__main__':
    voice_utils = VoiceUtils()
    #get_voice_and_text.get_effective_text()
    voice_utils.play_wav(recoder_file)




