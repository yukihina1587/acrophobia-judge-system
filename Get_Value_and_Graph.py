# -*- coding: utf-8 -*-
import sys, os
from Arduino import Get_ECG
import socket
import re
import concurrent.futures
import numpy as np

# グラフの描画
import matplotlib.pyplot as plt
import pylab
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Arduino')

connecting_eeg_flag = False


# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
def get_eeg():
    global connecting_eeg_flag
    attention = 0
    meditation = 0
    attention_array = np.zeros(50)
    meditation_array = np.zeros(50)
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
                    connecting_eeg_flag = True
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
                        else:
                            meditation = 0

                        print('meditation : ', meditation)
                        # return_confirm_m = ('Received: ' + str(meditation)).encode(encoding='utf-8')
                        # クライアントにデータを返す(b -> byte でないといけない)
                        # conn.sendall(return_confirm_m)

                        meditation_array = np.append(meditation_array, meditation)
                        meditation_array = np.delete(meditation_array, 0)

                    if not data:
                        break
        connecting_eeg_flag = False


def draw_graph():

    #  数直線
    fig, ax = plt.subplots(figsize=(10, 10))  # 画像サイズ
    fig.set_figheight(1)  # 高さ調整
    ax.tick_params(labelbottom=True, bottom=False)  # x軸設定
    ax.tick_params(labelleft=False, left=False)  # y軸設定
    print(Get_ECG.get_ecg())
    # 数直線上の数値を表示
    while Get_ECG.get_ecg() or connecting_eeg_flag:
        try:
            print('a')
            xmin = 0  # 数直線x軸の最小値
            xmax = 100  # 数直線x軸の最大値
            ymin = 0  # 数直線y軸の最小値
            ymax = max(heart_sampling_value)  # 数直線y軸の最大値
            print(heart_sampling_value)
            plt.tight_layout()  # グラフの自動調整
            plt.scatter(get_eeg().meditation_array, heart_sampling_value, s=10, c='r')  # 散布図
            # plt.hlines(y=0, xmin=xmin, xmax=xmax)  # 横軸
            # plt.vlines(x=[i for i in range(xmin, xmax + 1, 1)], ymin=-0.04, ymax=0.04)  # 目盛り線（大）
            # plt.vlines(x=[i / 10 for i in range(xmin * 10, xmax * 10 + 1, 1)], ymin=-0.02,
            #           ymax=0.02)  # 目盛り線（小）
            line_width = 1.5  # 目盛り数値の刻み幅
            plt.xticks(np.arange(xmin, xmax + line_width, line_width))  # 目盛り数値
            pylab.box(False)  # 枠を消す
            plt.pause(.01)
        except KeyboardInterrupt:
            plt.close()
            pylab.close()


if __name__ == "__main__":
    heart_sampling_value = np.zeros(50)

    # マルチスレッドでECGデータとEEGデータの取得を行う
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    executor.submit(Get_ECG.get_ecg)
    executor.submit(get_eeg)
    executor.submit(draw_graph)
