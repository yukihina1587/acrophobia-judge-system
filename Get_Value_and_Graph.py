# -*- coding: utf-8 -*-
import sys, os
from Arduino import Get_ECG
import socket
import re
import concurrent.futures
from multiprocessing import Value, Array, Process
import numpy as np
import datetime

# グラフの描画
import matplotlib.pyplot as plt
import pylab
import matplotlib.gridspec as gridspec

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Arduino')

connecting_eeg_flag = False
attention_array = np.zeros(50)
meditation_array = np.zeros(50)
i = 0


# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
def get_eeg(default_threashold, connecting_ecg_flag, heart_sampling_value, meditation_sampling_value):
    # 変数の初期化
    global connecting_eeg_flag
    attention = 0
    meditation = 0
    global attention_array
    global meditation_array
    i = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # IPアドレスとポートを指定
        s.bind(('127.0.0.1', 50007))
        # 1 接続
        s.listen(1)
        # connection するまで待つ
        while True:
            # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
            conn, addr = s.accept()
            with conn:
                while True:
                    # データを受け取る
                    data = conn.recv(4096)
                    data_str = data.decode('utf-8')
                    if 'a' in data_str:
                        # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                        # \D : 10進数でない任意の文字。（全角数字等を含む）
                        attention_num = re.sub("\\D", "", data_str)  # 数字のみをattentionとして代入
                        if attention_num != '':
                            attention = int(attention_num)
                        else:
                            attention = 0

                        # print('attention : ', attention)
                        # return_confirm_a = ('Received: ' + str(attention)).encode(encoding='utf-8')
                        # クライアントにデータを返す(b -> byte でないといけない)
                        # conn.sendall(return_confirm_a)

                        attention_array = np.append(attention_array, attention)
                        attention_array = np.delete(attention_array, 0)

                    elif 'm' in data_str:
                        # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                        # \D : 10進数でない任意の文字。（全角数字等を含む）
                        meditation_num = re.sub("\\D", "", data_str)  # 数字のみをmeditationとして代入
                        if meditation_num != '':
                            meditation = int(meditation_num)
                            i = i + 1
                        else:
                            meditation = 0

                        meditation_array = np.append(meditation_array, meditation)
                        meditation_array = np.delete(meditation_array, 0)

                        for m in range(50):
                            meditation_sampling_value[m] = meditation_array[m]

                        if i >= 51:
                            connecting_eeg_flag = True
                        elif i == 5:
                            print('脳波：しばらくお待ち下さい')
                        elif i == 40:
                            print('脳波：残り数ステップです')
                        elif (45 < i) and (i <= 50):
                            print('脳波：残り', (51 - i), 'ステップです')

                    if not data:
                        break


def draw_graph(default_threshold, connecting_ecg_flag, heart_sampling_value, meditation_sampling_value):
    # fig = plt.figure(figsize=(10, 10), facecolor="skyblue", linewidth=10, edgecolor="green")
    # fig.set_figheight(10)  # 高さ調整
    # fig.set_figwidth(10)  # 幅調整
    # gs = gridspec.GridSpec(5, 2)
    # plt.tick_params(labelbottom=True, bottom=True)  # x軸設定
    # plt.tick_params(labelleft=True, left=False)  # y軸設定
    # 数直線上の数値を表示

    while True:
        # print(Get_ECG.get_ecg_flag(), connecting_eeg_flag)
        # print(count.value)
        # print(meditation_sampling_value[:])
        dt_now = datetime.datetime.now()
        if (connecting_ecg_flag.value == 1) and (connecting_eeg_flag is True):
            # print('1')
            try:
                xmin = 0  # 数直線x軸の最小値
                xmax = 100  # 数直線x軸の最大値
                xmid = (xmin + xmax) / 2
                ymin = 0.5  # 数直線y軸の最小値
                ymax = 1.0  # 数直線y軸の最大値
                ymid = default_threshold.Value

                fig = plt.figure(figsize=(10, 10), facecolor="skyblue", linewidth=10, edgecolor="green")
                fig.set_figheight(10)  # 高さ調整
                fig.set_figwidth(10)  # 幅調整
                gs = gridspec.GridSpec(5, 2)
                plt.tick_params(labelbottom=True, bottom=True)  # x軸設定
                plt.tick_params(labelleft=True, left=False)  # y軸設定
                # 数直線上の数値を表示
                fear_state_time = np.zeros(100)
                # print(heart_sampling_value[:])
                # print(meditation_sampling_value[:])
                plt.tight_layout()  # グラフの自動調整
                # print(meditation_sampling_value[:])
                axA = plt.subplot(gs[:3, :])  # gs[0, 0]  ⇒ 左上, gs[0, :]  ⇒ 1行目すべて, gs[:, -1] ⇒ 最終列すべて
                if (heart_sampling_value[49] < 1.0) and (heart_sampling_value[49] > 0.55):
                    plt.scatter(meditation_sampling_value, heart_sampling_value, s=10, c="orange", alpha=0.3)  # 散布図
                axA.hlines([ymid], xmin, xmax, color='black')  # x_hlines
                axA.vlines([xmid], ymin, ymax, color='black')  # y_hlines
                x_line_width = 10  # x軸目盛り数値の刻み幅
                y_line_width = 0.1  # y軸目盛り数値の刻み幅
                plt.xticks(np.arange(xmin, xmax + x_line_width, x_line_width))  # x軸目盛り数値
                plt.yticks(np.arange(ymin, ymax + y_line_width, y_line_width))  # y軸目盛り数値
                axU = plt.subplot(gs[4, 1])
                axUR = plt.subplot(gs[4, 0])
                if meditation_sampling_value[49] < 50 and heart_sampling_value[49] > ymid:
                    axU.tick_params(labelbottom=False, bottom=False)  # x軸設定
                    axU.tick_params(labelleft=False, left=False)  # y軸設定
                    axU.text(0.6, 0.2, "Fear_State", size=40, color="blue")
                    fear_state_time = np.append(fear_state_time, dt_now)
                    fear_state_time = np.delete(fear_state_time, 0)
                    axUR.tick_params(labelbottom=False, bottom=False)  # x軸設定
                    axUR.tick_params(labelleft=False, left=False)  # y軸設定
                    fear_time = "{}\nこんにちは"
                    axUR.text(0.1, 0.5, fear_time.format(dt_now), size=20, color="black")
                    print(dt_now)

                else:
                    axU.cla()
                    axU.tick_params(labelbottom=False, bottom=False)  # x軸設定
                    axU.tick_params(labelleft=False, left=False)  # y軸設定
                    axU.text(0.6, 0.2, "", size=40, color="blue")
                pylab.box(False)  # 枠を消す
                plt.pause(.01)

            except KeyboardInterrupt:
                plt.close()
                pylab.close()


if __name__ == "__main__":
    # マルチスレッドでECGデータとEEGデータの取得を行う
    # 共有メモリの作成
    # Valueオブジェクトの生成
    count = Value('i', 0)
    connecting_ecg_flag = Value('i', 0)
    # Arrayオブジェクトの生成
    heart_sampling_value = Array('f', 50)
    meditation_sampling_value = Array('f', 50)

    process1 = Process(target=Get_ECG.get_ecg, args=[count, connecting_ecg_flag, heart_sampling_value, meditation_sampling_value])
    process2 = Process(target=get_eeg, args=[count, connecting_ecg_flag, heart_sampling_value, meditation_sampling_value])
    process3 = Process(target=draw_graph, args=[count, connecting_ecg_flag, heart_sampling_value, meditation_sampling_value])

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()


    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # executor.submit(Get_ECG.get_ecg)
    # executor.submit(get_eeg)
