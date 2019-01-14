# coding: utf-8
# LSTMを用いたRNN

# Kerasとその他ライブラリをインポート
#import keras
#from keras.models import Sequential
#from keras.layers import Dense, Activation
#from keras.layers.recurrent import LSTM
#from keras.optimizers import Adam
#from keras.callbacks import EarlyStopping
#import numpy as np
import matplotlib
# AGG(Anti-Grain Geometry engine)  pngで出力できる
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

import copy

f = open("2018-11-07.txt","r")
xlist = list()
ylist = list()
pulse = []

for line in f:
    s = line.split("|")
    if(len(s) >= 2 and s[1] != "   TIME   "):
        # print(s[1])
        xx = s[1]
        xxtime = dt.strptime(xx, ' %H:%M:%S ')
        yy = s[2]
        pulse.append(int(s[2]))
        #if(xx.find('03:00') > -1):
        if(xxtime.hour >= 3 and xxtime.minute >= 0 and xxtime.second >= 0):
            xlist.append(xx)
            ylist.append(yy)
            #if(xx.find('04:00') > -1):
            if(xxtime.hour == 3 and xxtime.minute == 9 and xxtime.second <= 59):
                break
f.close()

rate = 0
n = []
for p in range(50):
    n.append(pulse[p+1] - pulse[p])
    if n[p] >= 2 :
        rate += 1

# rate = [num for num in n if num >= 5]
# print(len(rate))

pNN50 = rate / 50
print("pNN50:", pNN50)


plt.figure(figsize=(20, 20))
plt.plot(xlist , ylist)
#plt.xticks(["00:00","03:00","06:00","09:00","12:00","15:00","18:00","21:00"])
#plt.yticks([50,60,70,80,90,100,110,120,130])
plt.title('pulse data')
plt.xlabel("time")
plt.ylabel("pulse")
#plt.savefig("pulse(2018-11-07).png")
# # 乱数を生成
# x = np.random.rand(100)
# y = np.random.rand(100)
#
# # 散布図を描画
# plt.scatter(x, y)
plt.show()

# def fear_judge():