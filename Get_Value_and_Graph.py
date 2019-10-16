# -*- coding: utf-8 -*-
#import sys, os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Arduino')
#from Arduino import Get_ECG
import socket

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
                    data = conn.recv(1024)
                    if data.decode('utf-8') == 'a':
                        attention = conn.recv(1024)
                        print('data : {}, addr: {}, value: {}'.format(data, addr, attention))
                    elif data.decode('utf-8') == 'm':
                        meditation = conn.recv(1024)
                    if not data:
                        break
                    # クライアントにデータを返す(b -> byte でないといけない)
                    print(data)
                    conn.sendall(b'Received: ' + data)