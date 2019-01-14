# coding: utf-8
# LSTMを使ったRNN

# Kerasとその他ライブラリをインポート
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras import metrics

import texttable as ttb

# CSVファイルから気象データをDataFrame型で取得する
def get_dfWeather_data():
    # 最初のカラム(年月日)をindexとし、最初の5行を読み飛ばす
    dfWeather = pd.read_csv('data_sapporo1975-2017.csv', index_col=0, parse_dates=True, skiprows = 5, encoding = 'shift_jis', header=None)
    # 不要な列を削除する
    dfWeather = dfWeather.drop([3, 4, 6, 8, 10, 11, 12, 14, 15, 17, 19, 20, 21, 23, 24, 26, 28, 29, 30, 32, 33, 35, 37, 38, 39, 41, 42, 44, 46, 47, 49, 51, 53, 54, 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79], axis=1)
    # 列名を指定する
    dfWeather.columns = [
        'day_of_the_week',            # 曜日
        'average_temperature',        # 平均気温(℃)
        'average_temperature_avg',    # 平均気温_平年(℃)
        'average_temperature_diff',   # 平均気温_平年差(℃)
        (中略)
        'average_cloud_cover',        # 平均雲量(10分比)
        'average_cloud_cover_avg',    # 平均雲量_平年(10分比)
        'average_cloud_cover_diff'    # 平均雲量_平年差(10分比)
    ]

    return dfWeather