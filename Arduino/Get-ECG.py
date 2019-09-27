# -*- coding: utf-8 -*-
import serial
import numpy as np
from scipy import signal
## scipyのモジュールを使う
from scipy.interpolate import Akima1DInterpolator
## 図示のために使うもの
import seaborn as sns
## フィッティングに使うもの
from scipy.optimize import curve_fit
## 平方根の計算
import math
# グラフの描画
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

class GraphWindow():
    # pyqugraph コンフィグ
    # Application
    app = QtGui.QApplication([])
    app.quitOnLastWindowClosed()
    # Window
    mainWindow = QtGui.QMainWindow()
    mainWindow.setWindowTitle("RRI_Analyzer")
    # Layout
    mainWindow.resize(800, 300)
    centralWid = QtGui.QWidget()
    mainWindow.setCentralWidget(centralWid)
    lay = QtGui.QVBoxLayout()
    centralWid.setLayout(lay)
    # Data Setting in the Figure
    RRIWid = pg.PlotWidget(name="RRI")
    RRIItem = RRIWid.getPlotItem()
    mainWindow.plotitem.setMouseEnabled(y=False)
    RRIItem.setYRange(0, 500)
    RRIItem.setXRange(0, 1000)
    # Axis
    RRIAxis = RRIItem.getAxis("bottom")
    RRIAxis.setLabel("rMSSD_data")
    #RRIAxis.setScale(fs / 2. / (fftLen / 2 + 1))
    #hz_interval = 500
    #newXAxis = (arange(int(fs / 2 / hz_interval)) + 1) * hz_interval
    #oriXAxis = newXAxis / (fs / 2. / (fftLen / 2 + 1))
    #RRIAxis.setTicks([zip(oriXAxis, newXAxis)])
    # キャンパスにのせる
    lay.addWidget(RRIWid)
    # ウィンドウ表示
    mainWindow.show()

class RRI_Analyzer():
    with serial.Serial('COM6',115200,timeout=1) as ser:
        # 初期化
        # 変数宣言
        i = 0
        x = np.zeros(50)
        y = np.zeros(50)
        rMSSD_array = np.zeros(50)
        status = False
        sampling_data_set = 50

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

                if i > 50:
                    SDNN_sigma = 0
                    rMSSD_sigma = 0
                    SDNN = 0
                    rMSSD = 0

                    # RRIの平均・分散を計算
                    s = sum(y)
                    N = len(y)
                    ave_RRI = s / N

                    for index in range(sampling_data_set):
                        SDNN_sigma += (y[index] - ave_RRI) ** 2

                    for index in range(sampling_data_set-1):
                        rMSSD_sigma += (y[index] - y[index+1]) ** 2

                    SDNN = math.sqrt(SDNN_sigma / 50)
                    rMSSD = math.sqrt(rMSSD_sigma / (50-1))

                    rMSSD_array = np.append(rMSSD_array, rMSSD)
                    rMSSD_array = np.delete(rMSSD_array, 0)
                    #print(rMSSD_array)
                    mainWin = GraphWindow()
                    mainWin.show()
                    sys.exit(app.exec_())
                elif i < 40:
                    print('しばらくお待ち下さい')
                elif 40 <= i and i < 45:
                    print('残り数ステップです')
                else:
                    print('残り', (51 - i),'ステップです')

        except KeyboardInterrupt:
            ser.close()

if __name__=="__main__":
    RRI_Analyzer()