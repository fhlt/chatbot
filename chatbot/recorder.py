#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyaudio import PyAudio, paInt16
import numpy as np
import subprocess
import os
from datetime import datetime
from log import THRESHOLD
import wave

class recoder:
    NUM_SAMPLES = 2000      #pyaudio内置缓冲大小
    SAMPLING_RATE = 8000    #取样频率
    LEVEL = 6000         #声音保存的阈值
    COUNT_NUM = 20      #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 5     #声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 60     #录音时间，单位s

    Voice_String = []

    # 播放wav格式音频文件
    def playwav(self, filename):
        # open a wave file, and return a Wave_read object
        wf = wave.open(filename, 'rb')
        pa = PyAudio()
        stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)
        while data.__len__() != 0:        # 判断是否结束
            stream.write(data)  # 从wf中读数据，然后写到stream中。就是从文件中读取数据然后写到声卡里
#            print(data.__len__())
            data = wf.readframes(1024)  # 从音频流中读取1024个采样数据，data类型为str.注意对音频流的读写都是字符串

        # stop stream
        stream.stop_stream()
        stream.close()
        wf.close()
        # close pyAudio
        pa.terminate()

    # 保存wav格式文件
    def savewav(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(self.Voice_String).tostring())
        # wf.writeframes(self.Voice_String.decode())
        wf.close()

    # 录音
    def recoder(self):
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        time_count = self.TIME_COUNT

        while True:
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum(audio_data > self.LEVEL)
            print 'db:', np.max(audio_data)
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            if save_count < 0:
                save_count = 0

            if save_count > 0:
            # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append(string_audio_data)
            else:
            #print save_buffer
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0:
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
            if time_count == 0:
                if len(save_buffer) > 0:
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False

if __name__ == "__main__":

    r = recoder()
    r.recoder()
    r.savewav("test.wav")
    # 翻译为中文
#    os.system("ffmpeg -i E://pyDoc//voiceTest//out.mp3  E://pyDoc//voiceTest//out.wav")
#    p = subprocess.Popen("ffmpeg -i E://pyDoc//voiceTest//out.mp3  E://pyDoc//voiceTest//out.wav", shell=True)
#    os.popen3('ffmpeg -i E://pyDoc//voiceTest//out.mp3  E://pyDoc//voiceTest//out.wav')
#    subprocess.call(["ffmpeg -i E://pyDoc//voiceTest//out.mp3 E://pyDoc//voiceTest//out.wav"], shell=True, cwd="E://pyDoc//voiceTest")
#    subprocess.call(["ffmpeg", "-i", "E://pyDoc//voiceTest//out.mp3", "E://pyDoc//voiceTest//out.wav"], shell=True)
#    r.playwav("test.wav")



