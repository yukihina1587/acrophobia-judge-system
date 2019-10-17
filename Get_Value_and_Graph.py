# -*- coding: utf-8 -*-
import sys, os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Arduino')
#from Arduino import Get_ECG
import socket
import re

# AF = IPv4 という意味
# TCP/IP の場合は、SOCK_STREAM を使う
if __name__=="__main__":
    #heartValue = Get_ECG.Get_ECG()

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
                        print(data_str)
                        # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                        # \D : 10進数でない任意の文字。（全角数字等を含む）
                        attention = int(re.sub("\\D", "", data_str))  # 数字のみをattentionとして代入
                        #print('attention : ', attention)
                    elif 'm' in data_str:
                        print(data_str)
                        # re.sub(正規表現パターン, 置換後文字列, 置換したい文字列)
                        # \D : 10進数でない任意の文字。（全角数字等を含む）
                        meditation = int(re.sub("\\D", "", data_str))  # 数字のみをmeditationとして代入
                        #print('meditation : ', meditation)
                    if not data:
                        break
                    # クライアントにデータを返す(b -> byte でないといけない)
                    conn.sendall(b'Received: ' + data)