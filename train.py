import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import librosa
from IPython.display import Audio
import pickle

df = pd.read_csv('cv-valid-train.csv')
df = df[~df['gender'].isna()]
df.shape

k = df[df['gender']=='male'].sample(n=50)
k2 = df[df['gender']=='female'].sample(n=50)
k.shape

final_data = pd.concat([k,k2]).sample(frac=1)
final_data.head()
# final_data.shape

#BASE_DIR = 'cv-valid-train/'
BASE_DIR = ''
X_train,y_train=[],[]
for i in tqdm(final_data.index):
    file = BASE_DIR + final_data.loc[i,'filename']
    wf, sr = librosa.load(file)
    mfcc_wf = librosa.feature.mfcc(y=wf,sr=sr)
    b = tf.keras.utils.pad_sequences(mfcc_wf,padding='post',maxlen=200)
    X_train.append(b)
    if final_data.loc[i,'gender'] == 'male':
        y_train.append(1)
    else:
        y_train.append(0)

X_train = np.array(X_train)
X_train.shape

y_train = np.array(y_train)
y_train.shape

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(20,200,)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256,activation='relu',kernel_regularizer=tf.keras.regularizers.l2()),
    tf.keras.layers.Dense(128,activation='relu',kernel_regularizer=tf.keras.regularizers.l2()),
    tf.keras.layers.Dense(64,activation='relu',kernel_regularizer=tf.keras.regularizers.l2()),
    tf.keras.layers.Dense(1,activation='sigmoid')
])
model.summary()

model.compile(optimizer='adam',loss=tf.keras.losses.BinaryCrossentropy(),metrics=['accuracy'])
history = model.fit(X_train,y_train,epochs=64,validation_split=0.2)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

from sklearn.metrics import classification_report
y_pred = model.predict(X_train)
y_pred.reshape(-1)
y_pred = [1 if x>0.5 else 0 for x in y_pred]
y_pred = np.array(y_pred)
y_train.reshape((100,1))
rep = classification_report(y_train,y_pred)

plt.plot(rep)
plt.show()

# wf, sr = librosa.load('cv-valid-train/sample-000015.mp3')
# mfcc_wf = librosa.feature.mfcc(y=wf,sr=sr)
# b = tf.keras.utils.pad_sequences(mfcc_wf,padding='post',maxlen=200)
# model.predict(np.array([b]))
# test the accuracy of the model

_, acc = model.evaluate(X_train, y_train, verbose=0)
print('> %.3f' % (acc * 100.0))


model.save('/model')
