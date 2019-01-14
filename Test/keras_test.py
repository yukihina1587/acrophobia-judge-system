%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import keras
df = pd.read_csv("AirportPassengers.csv",delimiter=";").dropna()
data = []
target = []
max_len = 24
dim = 1
# 正規化
maximum = df.Passengers.max()
minimum = df.Passengers.min()
df["Passengers"] = (df.Passengers-minimum)/(maximum-minimum)
# データを箱に入れる
for i in range(len(df)-max_len-1):
    data.append(df.Passengers.values[i:i+max_len])
    target.append(df.Passengers.values[i+max_len+1])
# データの整形
data = np.array(data).reshape(len(data),max_len,dim)
target = np.array(target).reshape(-1,1)
# データの分割
from sklearn.model_selection import train_test_split
N_train = int(len(data)*0.7)
N_test = len(data) - N_train
X_train, X_validation, Y_train, Y_validation = train_test_split(data, target, test_size=N_test)