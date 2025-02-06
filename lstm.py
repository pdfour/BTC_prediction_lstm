import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas import to_datetime
import math, time
import itertools
from sklearn import preprocessing
import datetime
from operator import itemgetter
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM
from keras.models import load_model
import keras
import h5py
import requests
import os


data_ =  pd.read_csv("./btc.csv",sep=",", index_col = 0)

data__ = data_.loc[:, ['date','open','high','low','close','Volume BTC']]
data_df = data__.tail(2000)


print("tableau de donnees")
print(data_df.tail(30))


print('\n')
print("dimensions des donnees")
print(data_df.shape)


"""
droping_list_all=[]
for j in range(0,7):
    if not df.iloc[:, j].notnull().all():
        droping_list_all.append(j)        
droping_list_all
"""

print('\n')
print("valeurs nulles")
print(data_df.isnull().sum())

"""
data_df['unix'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
"""

plt.plot(data_df['close'])
plt.show()


min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
dataset = min_max_scaler.fit_transform(data_df['close'].values.reshape(-1, 1))

print("donnees normalisees")
print(dataset[0:10])


train_size = int(len(dataset) * 0.7)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

print("taille des donnees d entrainement et de test")
print(len(train), len(test))

print('\n')

def create_dataset(dataset, fenetre=15):
    dataX, dataY = [], []
    for i in range(len(dataset)-fenetre-1):
        a = dataset[i:(i+fenetre), 0]
        dataX.append(a)
        dataY.append(dataset[i + fenetre, 0])
    return np.array(dataX), np.array(dataY)


x_train, y_train = create_dataset(train, fenetre=15)
x_test, y_test = create_dataset(test, fenetre=15)

print("dimensions des donnees d'entrainement et de test")

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)


print('\n')
x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

print("dimensions des donnees d'entrainement et de test apres redimensionnement")

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)


# entrainement
fenetre = 15
model = Sequential()
model.add(LSTM(20, input_shape=(1, fenetre)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=200, batch_size=1, verbose=2)


#prediction
trainprediction = model.predict(x_train)
testprediction = model.predict(x_test)


trainprediction = min_max_scaler.inverse_transform(trainprediction)
trainY = min_max_scaler.inverse_transform([y_train])
testprediction = min_max_scaler.inverse_transform(testprediction)
testY = min_max_scaler.inverse_transform([y_test])

# calcul du RMSE
trainScore = math.sqrt(mean_squared_error(trainY[0], trainprediction[:,0]))
print('Score d entrainement: %.2f RMSE' % (trainScore   ))
testScore = math.sqrt(mean_squared_error(testY[0], testprediction[:,0]))
print('Score de test: %.2f RMSE' % (testScore))



# on ajoute les données d'entrainement au graphique avec decalage
trainpredictionPlot = np.empty_like(dataset)
trainpredictionPlot[:, :] = np.nan
trainpredictionPlot[fenetre:len(trainprediction)+fenetre, :] = trainprediction

# on ajoute les données de test au graphique avec decalage
testpredictionPlot = np.empty_like(dataset)
testpredictionPlot[:, :] = np.nan
testpredictionPlot[len(trainprediction)+(fenetre*2)+1:len(dataset)-1, :] = testprediction

# graphique
plt.plot(min_max_scaler.inverse_transform(dataset))
plt.plot(trainpredictionPlot)
plt.plot(testpredictionPlot)
plt.show()
