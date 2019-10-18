# -*- coding: utf-8 -*-
import sys, os
from Arduino import Get_ECG
import socket
import re
import concurrent.futures

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Arduino')


# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
if __name__ == "__main__":
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    heart_sampling_value = executor.submit(Get_ECG.get_ecg())
    brainwave_value = executor.submit(get_eeg())

    print(heart_sampling_value)


def get_eeg():
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
                    attention = 0
                    meditation = 0
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

                        print('attention : ', attention)
                        # return_confirm_a = ('Received: ' + str(attention)).encode(encoding='utf-8')
                        # クライアントにデータを返す(b -> byte でないといけない)
                        # conn.sendall(return_confirm_a)

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
                    if not data:
                        break
