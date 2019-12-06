# -*- coding: utf-8 -*-
import serial
import numpy as np
# 平方根の計算
import math
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '..')
import csv
import datetime


def get_ecg(default_threshold, ecg_flag, username, heart_value, medi_array):

    with serial.Serial('COM3', 115200, timeout=0) as ser:
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
        sdnn_sigma = 0
        rmssd_sigma = 0
        sdnn = 0
        rmssd = 0
        ratio = 0
        ave = 0

        while True:
            try:
                dt_now = datetime.datetime.now()
                rri_data = ser.read_all()
                rri_data_str = rri_data.decode('utf-8')

                if rri_data_str != '':
                    int_data = int(rri_data_str)

                    if (50 < int_data) and (int_data < 300):
                        # 配列をキューと見たてて要素を追加・削除
                        x = np.append(x, int_data)
                        x = np.delete(x, 0)

                        if x[0] > 50:
                            # RRIの平均・分散を計算
                            s = sum(x)
                            N = len(x)
                            ave_rri = s / N

                            for index in range(sampling_data_set):
                                sdnn_sigma += (x[index] - ave_rri) ** 2

                            for index in range(sampling_data_set - 1):
                                rmssd_sigma += (x[index] - x[index + 1]) ** 2

                            sdnn = math.sqrt(sdnn_sigma / 50)
                            rmssd = math.sqrt(rmssd_sigma / (50 - 1))

                            ratio = sdnn / rmssd

                            if (ratio > 0.4) and (ratio < 1.2):
                                ratio_array = np.append(ratio_array, ratio)
                                ratio_array = np.delete(ratio_array, 0)

                                if ratio_array[0] > 0.5:
                                    ecg_flag.value = 1

                                    if not threshold_flag:
                                        threshold_flag = True
                                        default_sum = sum(ratio_array)
                                        ave = default_sum / 50
                                        default_threshold.value = ave

                                    for l in range(sampling_data_set):
                                        heart_value[l] = ratio_array[l]

                                    filename = 'データ/' + str(username) + dt_now.strftime('%Y-%m-%d-%H:%M') \
                                               + 'vital_info.csv'
                                    with open(filename, 'a') as f:
                                        writer = csv.writer(f)
                                        writer.writerow(dt_now.strftime('%Y-%m-%d %H:%M:%S'))
                                        writer.writerow(medi_array)
                                        writer.writerow(ratio_array)

                                elif ratio_array[45] > 0.5 and ratio_array[44] == 0:
                                    print('心拍：しばらくお待ち下さい')
                                elif ratio_array[10] > 0.5 and ratio_array[9] == 0:
                                    print('心拍：残り数ステップです')
                                elif ratio_array[0] > 0.5:
                                    print('心拍：準備が整いました')

            except KeyboardInterrupt:
                ser.close()
                ecg_flag.value = 0
                break
