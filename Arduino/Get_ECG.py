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
import pylab
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '..')
import Get_Value_and_Graph
import time


def get_ecg():
    with serial.Serial('COM6', 115200, timeout=0) as ser:
        # 初期化
        i = 0
        x = np.zeros(50)
        y = np.zeros(50)
        ratio_array = np.zeros(50)
        eeg_array = np.zeros(50)
        status = False
        sampling_data_set = 50
        int_data = 0

        #  数直線
        fig, ax = plt.subplots(figsize=(10, 10))  # 画像サイズ
        fig.set_figheight(1)  # 高さ調整
        ax.tick_params(labelbottom=True, bottom=False)  # x軸設定
        ax.tick_params(labelleft=False, left=False)  # y軸設定
        # 数直線上の数値を表示

        while True:
            try:
                rri_data = ser.read_all()
                rri_data_str = rri_data.decode('utf-8')

                if rri_data_str != '':
                    int_data = int(rri_data_str)
                    i = i + 1

                    if (50 < int_data) and (int_data < 300):
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
                        ratio = 0

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

                        ratio = sdnn / rmssd

                        Get_Value_and_Graph.heart_sampling_value = ratio

                        ratio_array = np.append(ratio_array, ratio)
                        ratio_array = np.delete(ratio_array, 0)

                        xmin = 0  # 数直線の最小値
                        xmax = max(ratio_array)  # 数直線の最大値
                        plt.tight_layout()  # グラフの自動調整
                        plt.scatter(ratio_array, eeg_array, s=10, c='r')  # 散布図
                        #plt.hlines(y=0, xmin=xmin, xmax=xmax)  # 横軸
                        #plt.vlines(x=[i for i in range(xmin, xmax + 1, 1)], ymin=-0.04, ymax=0.04)  # 目盛り線（大）
                        #plt.vlines(x=[i / 10 for i in range(xmin * 10, xmax * 10 + 1, 1)], ymin=-0.02,
                        #           ymax=0.02)  # 目盛り線（小）
                        line_width = 10  # 目盛り数値の刻み幅
                        plt.xticks(np.arange(xmin, xmax + line_width, line_width))  # 目盛り数値
                        pylab.box(False)  # 枠を消す
                        plt.pause(.01)

                        if rmssd > 150:
                            print('y:', y)
                            print('s:', s)
                            print('N:', N)
                            print('ave:', ave_rri)
                            print('rmssd_sigma:', rmssd_sigma)
                            print('rmssd:', rmssd)
                            print('-------------')

                        print(ratio)

                    elif i == 5:
                        print('しばらくお待ち下さい')
                    elif i == 40:
                        print('残り数ステップです')
                    elif (45 < i) and (i <= 50):
                        print('残り', (51 - i), 'ステップです')

            except KeyboardInterrupt:
                plt.close()
                pylab.close()
                ser.close()

def aaa():
    while True:
        print("aaa")
        time.sleep(1)