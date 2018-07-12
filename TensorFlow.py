# coding: utf-8
# Conv2Dを使ったCNN

# CNN Model1 - one layer
# Kerasとその他ライブラリをインポート
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Conv2D, Dropout
from keras.utils import np_utils
from keras.optimizers import SGD

# Windowsの場合は以下を入力
import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\bin'

# 早期終了のためのCallbacksとデータ処理に必要なNumpyをインポート
import keras.callbacks as callbacks
import numpy as np

# ランダムな数値でダミーデータを用意
x_train = np.random.random((100, 6, 6, 1))
y_train = keras.utils.to_categorical(np.random.randiant(10, size=(100, 1)), num_classes=10)
x_test = np.random.random((20, 6, 6, 1))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)

# ドロップアウトを追加して畳み込みニューラルネットワークのモデルを作成
model = Sequential()
modl.add(Conv2D(filters=3, kernel_size=(3,3), input_shape=(6, 6, 1), padding='same', name='Conv2D_1'))
model.add(Dropout(rate=0.5, name='Dropout_1'))
model.add(Flatten(name='Flatten_1'))
model.add(Dense(units=10,activation='softmax', name='Dense_1'))