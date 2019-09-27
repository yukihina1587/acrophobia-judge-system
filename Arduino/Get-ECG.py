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

def main():
    with serial.Serial('COM6',115200,timeout=1) as ser:
        # 初期化
        i = 0
        x = np.zeros(50)
        y = np.zeros(50)
        rMSSD_array = np.zeros(50)
        status = False
        sampling_data_set = 50

        # MATPLOTLIB コンフィグ
        plt.ion()
        plt.figure(figsize=(30, 10), dpi=50)
        li, = plt.plot(x, y)
        plt.ylim(400)
        plt.title('ECG Graph', fontsize=18)
        plt.xlabel('ms', fontsize=18)
        plt.ylabel('ECG', fontsize=18)

        try:
            while True:
                RRI_data = ser.read()
                int_data = int.from_bytes(RRI_data, 'big')
                i = i + 1

                # 配列をキューと見たてて要素を追加・削除
                x = np.append(x, i)
                x = np.delete(x, 0)
                y = np.append(y, int_data)
                y = np.delete(y, 0)

                if i > 50:
                    SDNN_sigma = 0
                    rMSSD_sigma = 0
                    SDNN = 0
                    rMSSD = 0

                    # RRIの平均・分散を計算
                    s = sum(y)
                    N = len(y)
                    ave_RRI = s / N

                    for index in range(sampling_data_set):
                        SDNN_sigma += (y[index] - ave_RRI) ** 2

                    for index in range(sampling_data_set-1):
                        rMSSD_sigma += (y[index] - y[index+1]) ** 2

                    SDNN = math.sqrt(SDNN_sigma / 50)
                    rMSSD = math.sqrt(rMSSD_sigma / (50-1))

                    rMSSD_array = np.append(rMSSD_array, rMSSD)
                    rMSSD_array = np.delete(rMSSD_array, 0)
                    #print(rMSSD_array)

                    if (ave_RRI - int_data) > 20:
                        status = True
                        #print('恐怖状態')
                elif i < 40:
                    print('しばらくお待ち下さい')
                elif 40 <= i and i < 45:
                    print('残り数ステップです')
                else:
                    print('残り', (51 - i),'ステップです')

                li.set_xdata(x)
                li.set_ydata(y)
                plt.xlim((x.min(), x.max()))
                plt.ylim([-100, 300])
                plt.tick_params(labelsize=18)
                plt.pause(.01)

                plt.show()

        except KeyboardInterrupt:
            plt.close()
            ser.close()

if __name__=="__main__":
    main()