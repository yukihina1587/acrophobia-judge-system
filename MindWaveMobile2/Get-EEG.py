# -*- coding: utf-8 -*-
import thinkgear
# 正規表現操作のライブラリ
import re
import numpy as np

PORT = 'COM5'

attention = np.zeros()
meditation = 0

for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for pkt in packets:
        if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
            continue

        t = str(pkt)

        if t != '':
            if 'ATTENTION eSense:' in t:
                # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                # \D : 10進数でない任意の文字。（全角数字等を含む）
                attention = re.sub("\\D", "", t)  # 数字のみをattentionとして代入
                print('attention:',attention)
            if 'MEDITATION eSense:' in t:
                # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                # \D : 10進数でない任意の文字。（全角数字等を含む）
                meditation = re.sub("\\D", "", t)  # 数字のみをattentionとして代入
                print('meditation',meditation)

        #if int(attention) == 0:  # or int(meditation) == 0:
        #    continue
        #print "attention", attention
        # print "meditation", meditation

        #attention = int(attention)
        # meditation = float(meditation)