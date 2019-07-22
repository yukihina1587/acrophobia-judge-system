#coding utf-8
import serial
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def main():
    with serial.Serial('COM6',115200,timeout=1) as ser:
        # 初期化
        i = 0
        x = np.zeros(300)
        y = np.zeros(300)
        peak = np.zeros(300)

        N = 512  # サンプル数

        # MATPLOTLIB コンフィグ
        plt.ion()
        plt.figure(figsize=(30, 10), dpi=50)
        li, = plt.plot(x, y)
        plt.ylim(400)
        plt.title('EFG Graph', fontsize=18)
        plt.xlabel('ms', fontsize=18)
        plt.ylabel('EFG', fontsize=18)

        try:
            while True:
                String_data = ser.read()
                int_data = int.from_bytes(String_data, 'big')
                #print(int_data)
                i = i + 1

                # 配列をキューと見たてて要素を追加・削除
                x = np.append(x, i)
                x = np.delete(x, 0)
                y = np.append(y, int_data)
                y = np.delete(y, 0)
                #print(y)

                # 非線形関数で補間
                # https://qiita.com/hik0107/items/9bdc236600635a0e61e8

                # ピーク値のインデックスを取得
                # orderの値によって検出ピークの数が変わる
                # 例えば１だと前後各一点と比較してピーク値を算出、２だと前後二点と比較してピーク値を算出する
                maxid = signal.argrelmax(y, order=100)  # 最大値
                #minid = signal.argrelmin(y, order=100)  # 最小値

                plt.plot(x[maxid], y[maxid], 'ro')

                li.set_xdata(x)
                li.set_ydata(y)

                plt.xlim((x.min(), x.max()))
                plt.ylim([-100, 300])
                plt.tick_params(labelsize=18)
                plt.draw()
                plt.pause(.01)


                #plt.plot(x[minid], y[minid], 'bo')
                #plt.legend()
                plt.show()

        except KeyboardInterrupt:
            plt.close()
            ser.close()

        #while True:
            #c = ser.readline()
            #d = re.findall('[0-9]+\.+[0-9]',str(c),flags=0)
            #d = [float(i) for i in d]
            #for i in range(0, len(d)):  #要素を1つずつ順番に出力します
                #print(d[i])
            #print

if __name__=="__main__":
    main()