# coding: utf-8
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

#モデルに読み込ませるデータを生成する
def generate_data(data, length_per_unit, dimension):
    #時系列データを入れる箱
    sequences = []
    #正解データを入れる箱
    target = []
    #正解データの日時を入れる箱
    target_data = []
    