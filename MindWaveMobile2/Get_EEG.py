# -*- coding: utf-8 -*-
import thinkgear
# 正規表現操作のライブラリ
import re
import numpy as np
import socket
import struct

PORT = 'COM5'


def get_eeg():
    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        for pkt in packets:
            if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
                continue

            t = str(pkt)

            if t != '':
                if 'ATTENTION eSense:' in t:
                    # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                    # \D : 10進数でない任意の文字。（全角数字等を含む）
                    attention = int(re.sub("\\D", "", t))  # 数字のみをattentionとして代入
                    flag = 'a'
                    # print 'attention:', attention
                    send_eeg(flag, attention)
                if 'MEDITATION eSense:' in t:
                    # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                    # \D : 10進数でない任意の文字。（全角数字等を含む）
                    meditation = int(re.sub("\\D", "", t))  # 数字のみをmeditationとして代入
                    flag = 'm'
                    # print 'meditation', meditation
                    send_eeg(flag, meditation)


def send_eeg(flag, value):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    value = str(value)
    # サーバを指定
    s.connect(('127.0.0.1', 50007))
    # フラグと値の連結
    flag_and_value = flag + value
    # サーバにメッセージを送る
    s.sendall(flag_and_value)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    # data = s.recv(4096)
    # print(repr(data))
    # if str(data) != ('Received: ' + value):
        # print 'a'
        # send_eeg(flag, value)


if __name__ == "__main__":
    get_eeg()
