# -*- coding: utf-8 -*-
import serial
import numpy as np
# 平方根の計算
import math
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '..')
import csv
import pprint
import datetime


def get_ecg(default_threshold, ecg_flag, heart_value, medi_array):

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
        q = 0
        threshold_flag = False

        while True:
            try:
                dt_now = datetime.datetime.now()
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
                        ecg_flag.value = 1
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

                        if (i == 51 + q) and (ratio != 0) and (not threshold_flag):
                            q = q + 1
                            default_threshold.value = ratio
                            if default_threshold != 0:
                                threshold_flag = True

                        if (ratio > 0.4) and (ratio < 1.2):
                            ratio_array = np.append(ratio_array, ratio)
                            ratio_array = np.delete(ratio_array, 0)

                        # Get_Value_and_Graph.CollectDataAndGraph.set_ecg_sampling_data(ratio)
                        for l in range(50):
                            heart_value[l] = ratio_array[l]

                        with open('データ/heart_info.csv', 'a') as f:
                            writer = csv.writer(f)
                            # writer.writerow(dt_now)
                            writer.writerow(y)
                            writer.writerow(ratio_array)

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
                ecg_flag.value = 0
                break


def get_ecg_flag():
    return connecting_ecg_flag
