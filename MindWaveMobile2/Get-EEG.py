import thinkgear

PORT = 'COM5'

for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for pkt in packets:
        if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
            continue

        t = str(pkt)

        if t != '':
            differencer = t[0:1] # 最初の文字を取り出す
            if int(differencer) == 1:
                attention = t[1:]  # 最初の文字以外をattentionとして代入
                print(attention)