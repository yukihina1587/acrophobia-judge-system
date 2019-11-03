# -*- coding: utf-8 -*-
import sys, os
from Arduino import Get_ECG
import socket
import re
import concurrent.futures
from multiprocessing import Value, Array, Process
import numpy as np

# グラフの描画
import matplotlib.pyplot as plt
import pylab

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Arduino')

connecting_eeg_flag = False
attention_array = np.zeros(50)
meditation_array = np.zeros(50)
i = 0


# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
def get_eeg(count, array):
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

                        if i >= 51:
                            connecting_eeg_flag = True
                            CollectDataAndGraph.set_eeg_sampling_data(count, array, connecting_eeg_flag, meditation)
                            # print('meditation : ', meditation)
                        elif i == 5:
                            print('脳波：しばらくお待ち下さい')
                        elif i == 40:
                            print('脳波：残り数ステップです')
                        elif (45 < i) and (i <= 50):
                            print('脳波：残り', (51 - i), 'ステップです')

                    if not data:
                        break


def draw_graph():
    # 数直線
    fig, ax = plt.subplots(figsize=(10, 10))  # 画像サイズ
    fig.set_figheight(10)  # 高さ調整
    fig.set_figwidth(10)  # 幅調整
    ax.tick_params(labelbottom=True, bottom=False)  # x軸設定
    ax.tick_params(labelleft=True, left=False)  # y軸設定
    # 数直線上の数値を表示
    # print(Get_ECG.get_ecg_flag(), connecting_eeg_flag)
    if Get_ECG.get_ecg_flag() or connecting_eeg_flag:
        print('1')
        try:
            xmin = 0  # 数直線x軸の最小値
            xmax = 100  # 数直線x軸の最大値
            ymin = 0  # 数直線y軸の最小値
            ymax = max(heart_sampling_value)  # 数直線y軸の最大値
            print(heart_sampling_value)
            print(meditation_array)
            plt.tight_layout()  # グラフの自動調整
            plt.scatter(meditation_array, heart_sampling_value, s=10, c='r')  # 散布図
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
    else:
        print('3')


class CollectDataAndGraph:
    heart_sampling_value = np.zeros(50)
    meditation_sampling_value = np.zeros(50)
    i = 1

    @classmethod
    def set_ecg_sampling_data(self, data):
        self.heart_sampling_value = np.append(self.heart_sampling_value, data)
        self.heart_sampling_value = np.delete(self.heart_sampling_value, 0)
        print('ecg:', self.i)
        self.i = self.i + 1
        # self.heart_sampling_value = data

    @classmethod
    def set_eeg_sampling_data(self, count, array, flag, data):
        self.meditation_sampling_value = np.append(self.meditation_sampling_value, data)
        self.meditation_sampling_value = np.delete(self.meditation_sampling_value, 0)
        print('ecg:', array)
        print('eeg:', data)
        self.i = self.i + 1
        # self.meditation_sampling_value = data
        # draw_graph(flag)
        # print('a', self.heart_sampling_value)
        # print('b', self.meditation_sampling_value)

    def print(self):
        print('a', self.heart_sampling_value)
        print('b', self.meditation_sampling_value)


if __name__ == "__main__":
    # マルチスレッドでECGデータとEEGデータの取得を行う
    with Manager() as manager:
        # マネージャからValueクラスを作成
        count = manager.Value('i', 0)
        # マネージャからListを作成
        array = manager.list()

        process1 = Process(target=Get_ECG.get_ecg, args=[count, array])
        process2 = Process(target=get_eeg, args=[count, array])

        process1.start()
        process2.start()

        process1.join()
        process2.join()

    #executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    #executor.submit(Get_ECG.get_ecg)
    #executor.submit(get_eeg)
