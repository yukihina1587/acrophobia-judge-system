# -*- coding: utf-8 -*-
import thinkgear
# 正規表現操作のライブラリ
import re
import numpy as np
import socket
import struct

PORT = 'COM5'
attention = 0
meditation = 0

def Get_EEG():
    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        for pkt in packets:
            if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
                continue

            flag = ''
            t = str(pkt)

            if t != '':
                if 'ATTENTION eSense:' in t:
                    # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                    # \D : 10進数でない任意の文字。（全角数字等を含む）
                    attention = int(re.sub("\\D", "", t))  # 数字のみをattentionとして代入
                    flag = 'a'
                    print('attention:', attention)
                    Send_EEG(flag, attention)
                if 'MEDITATION eSense:' in t:
                    # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                    # \D : 10進数でない任意の文字。（全角数字等を含む）
                    meditation = int(re.sub("\\D", "", t))  # 数字のみをmeditationとして代入
                    flag = 'm'
                    print('meditation', meditation)
                    Send_EEG(flag, meditation)

            #if int(attention) == 0:  # or int(meditation) == 0:
            #    continue
            #print "attention", attention
            # print "meditation", meditation

        #attention = int(attention)
        # meditation = float(meditation)

def Send_EEG(flag,value):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #受け取ってきた値をバイトコードに変換
    value_byte = struct.pack('!i', value)
    # サーバを指定
    s.connect(('127.0.0.1', 50007))
    # サーバにメッセージを送る
    s.sendall(flag)
    s.sendall(value_byte)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    data = s.recv(1024)
    #data_int = struct.unpack('>b', data)
    print(repr(data))

if __name__=="__main__":
    Get_EEG()