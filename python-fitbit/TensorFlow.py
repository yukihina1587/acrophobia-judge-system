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

f = open("2018-11-07.txt","r")
xlist = list()
ylist = list()
for line in f:
    s = line.split("|")
    if(len(s) >= 2 and s[1] != "   TIME   "):
        # print(s[1])
        xx = s[1]
        yy = s[2]
        if(xx.find('03:00') > -1):
            xlist.append(xx)
            ylist.append(yy)
            if(xx.find('04:00') > -1):
                break
f.close()


plt.figure(figsize=(100, 20))
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
print("あああああ")
plt.show()

# def fear_judge():