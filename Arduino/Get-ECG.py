# -*- coding: utf-8 -*-
import serial
import numpy as np
from scipy import signal
## scipyのモジュールを使う
from scipy.interpolate import Akima1DInterpolator
## 図示のために使うもの
import seaborn as sns
## フィッティングに使うもの
from scipy.optimize import curve_fit
## 平方根の計算
import math
# グラフの描画
import matplotlib.pyplot as plt

import struct

def main():
    with serial.Serial('COM6', 115200, timeout=0) as ser:
        # 初期化
        i = 0
        x = np.zeros(50)
        y = np.zeros(50)
        rmssd_array = np.zeros(50)
        status = False
        sampling_data_set = 50
        int_data = 0

        # MATPLOTLIB コンフィグ
        plt.ion()
        plt.figure(figsize=(30, 10), dpi=50)
        li, = plt.plot(x, y)
        plt.title('ECG Graph', fontsize=18)
        plt.xlabel('ms', fontsize=18)
        plt.ylabel('rMSSD', fontsize=18)

        while True:
            try:
                rri_data = ser.read_all()
                rri_data_str = rri_data.decode('utf-8')

                if rri_data_str != '':
                    int_data = int(rri_data_str)
                    i = i + 1

                    # 配列をキューと見たてて要素を追加・削除
                    x = np.append(x, i)
                    x = np.delete(x, 0)
                    y = np.append(y, int_data)
                    y = np.delete(y, 0)

                    if i > 50:
                        sdnn_sigma = 0
                        rmssd_sigma = 0
                        sdnn = 0
                        rmssd = 0

                        # RRIの平均・分散を計算
                        s = sum(y)
                        N = len(y)
                        ave_rri = s / N

                        for index in range(sampling_data_set):
                            sdnn_sigma += (y[index] - ave_rri) ** 2

                        for index in range(sampling_data_set-1):
                            rmssd_sigma += (y[index] - y[index+1]) ** 2

                        sdnn = math.sqrt(sdnn_sigma / 50)
                        rmssd = math.sqrt(rmssd_sigma / (50-1))

                        rmssd_array = np.append(rmssd_array, rmssd)
                        rmssd_array = np.delete(rmssd_array, 0)

                        #print(rmssd_array)
                        li.set_ydata(rmssd_array)
                        li.set_xdata(x)
                        plt.xlim((x.min(), x.max()))
                        plt.ylim([-50, 100])
                        plt.tick_params(labelsize=18)
                        plt.pause(.01)
                        plt.show()
                    elif i == 0:
                        print('しばらくお待ち下さい')
                    elif i == 40:
                        print('残り数ステップです')
                    elif (45 < i) and (i <= 50):
                        print('残り', (51 - i), 'ステップです')

            except KeyboardInterrupt:
                plt.close()
                ser.close()

if __name__=="__main__":
    main()