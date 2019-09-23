#coding utf-8
import serial
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
## scipyのモジュールを使う
from scipy.interpolate import Akima1DInterpolator
## 図示のために使うもの
import seaborn as sns
##フィッティングに使うもの
from scipy.optimize import curve_fit
## 最頻値を求めるためのライブラリ
import statistics
## 最頻値を求める際に最初は配列には0しか存在しないため、2つ以上の最頻値を返してくる。その例外を回避するライブラリ
import collections

status = False

def spline_interp(in_x, in_y):
    f = Akima1DInterpolator(in_x, in_y)
    out_x = np.linspace(np.min(in_x), np.max(in_x), np.size(in_x)*100) # もとのxの個数より多いxを用意
    out_y = f(out_x)

    return out_x, out_y

def moving_avg(in_x, in_y):
    np_y_conv = np.convolve(in_y, np.ones(3)/float(3), mode='valid') # 畳み込む
    out_x_dat = np.linspace(np.min(in_x), np.max(in_x), np.size(np_y_conv))

    return out_x_dat, np_y_conv

def main():
    with serial.Serial('COM6',115200,timeout=1) as ser:
        # 初期化
        i = 0
        x = np.zeros(300)
        y = np.zeros(300)
        recent_condition = np.zeros(11)

        # MATPLOTLIB コンフィグ
        plt.ion()
        plt.figure(figsize=(30, 10), dpi=50)
        li, = plt.plot(x, y)
        plt.ylim(400)
        plt.title('ECG Graph', fontsize=18)
        plt.xlabel('ms', fontsize=18)
        plt.ylabel('ECG', fontsize=18)

        try:
            while True:
                RRI_data = ser.read()
                int_data = int.from_bytes(RRI_data, 'big')
                i = i + 1

                # 配列をキューと見たてて要素を追加・削除
                x = np.append(x, i)
                x = np.delete(x, 0)
                y = np.append(y, int_data)
                y = np.delete(y, 0)

                if int_data > 10:
                    recent_condition = np.append(recent_condition, int_data)
                    recent_condition = np.delete(recent_condition, 0)
                    ## default_RRI = statistics.mode(recent_condition)
                    # "statistics.StatisticsError: no unique mode; found 2 equally common values"という最頻値が2つ存在した場合に起こる例外の対策のためcounter()メソッドを使用
                    default_RRI = collections.Counter(recent_condition).most_common()[0][0]
                    ## recent_conditionもdefault_RRIも型確認を行うとfloat型で出力されている
                    ## print(default_RRI)
                    if default_RRI > int_data:
                        status = True
                        print("緊張状態")

                ## pythonのforループの以下のような構文ではiにはrecent_conditionの実際の値が格納されていく（index値ではない）
                #for i in recent_condition:
                    #if i < default_RRI:
                    #    status = True
                    #    print("緊張状態")

                # 移動平均で補間
                # https://www.snova301.work/entry/2018/10/07/135233

                # x1, y1 = spline_interp(x, y)
                # print[y1]

                # x2, y2 = moving_avg(x, y)
                # x3, y3 = spline_interp(x2, y2)

                # ピーク値のインデックスを取得
                # orderの値によって検出ピークの数が変わる
                # 例えば１だと前後各一点と比較してピーク値を算出、２だと前後二点と比較してピーク値を算出する
                #maxid = signal.argrelmax(y, order=100)  # 最大値
                #print(maxid)
                # minid = signal.argrelmin(y, order=100)  # 最小値

                #plt.plot(x[maxid], y[maxid], 'ro')

                li.set_xdata(x)
                li.set_ydata(y)

                plt.xlim((x.min(), x.max()))
                plt.ylim([-100, 300])
                plt.tick_params(labelsize=18)
                # plt.draw()
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