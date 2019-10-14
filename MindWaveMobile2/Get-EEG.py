# -*- coding: utf-8 -*-
import thinkgear

PORT = 'COM5'

attention = 0
meditation = 0

for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for pkt in packets:
        if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
            continue

        t = str(pkt)

        if t != '':
            print(t[0:1])
            #differencer = ''
            #differencer = t[0:1] # 最初の文字を取り出す
            #if int(differencer) == 1:
            #    attention = t[1:]  # 最初の文字以外をattentionとして代入
            #    print(attention)

        if int(attention) == 0:  # or int(meditation) == 0:
            continue
        print "attention", attention
        # print "meditation", meditation

        attention = int(attention)
        # meditation = float(meditation)