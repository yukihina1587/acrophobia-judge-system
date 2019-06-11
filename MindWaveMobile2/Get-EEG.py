import thinkgear

PORT = '/dev/tty.MindWaveMobile-SerialPo' /*ここに/dev/tty.~を記述
for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for p in packets:
        if isinstance(p, thinkgear.ThinkGearRawWaveData):
            continue
        print p