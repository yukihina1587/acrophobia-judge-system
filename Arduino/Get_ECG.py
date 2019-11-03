# -*- coding: utf-8 -*-
import serial
import numpy as np
# 平方根の計算
import math
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '..')
import Get_Value_and_Graph
from multiprocessing import Value, Array, Process

connecting_ecg_flag = False


def get_ecg(count, array):
    global connecting_ecg_flag
    print('get_ecg')
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
                        connecting_ecg_flag = True
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

                        ratio_array = np.append(ratio_array, ratio)
                        ratio_array = np.delete(ratio_array, 0)

                        # Get_Value_and_Graph.CollectDataAndGraph.set_ecg_sampling_data(ratio)
                        array.append(ratio)

                        if rmssd > 150:
                            print('y:', y)
                            print('s:', s)
                            print('N:', N)
                            print('ave:', ave_rri)
                            print('rmssd_sigma:', rmssd_sigma)
                            print('rmssd:', rmssd)
                            print('-------------')

                    elif i == 5:
                        print('心拍：しばらくお待ち下さい')
                    elif i == 40:
                        print('心拍：残り数ステップです')
                    elif (45 < i) and (i <= 50):
                        print('心拍：残り', (51 - i), 'ステップです')

            except KeyboardInterrupt:
                ser.close()
                connecting_ecg_flag = False
                break


def get_ecg_flag():
    return connecting_ecg_flag
