import tensorflow as tf
from tensorflow import one_hot
from tensorflow import keras as k
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

(X_train, Y_train), (X_test, Y_test) = k.datasets.mnist.load_data()

X_train = X_train/255
X_test = X_test/255

Y_train = tf.one_hot(Y_train, 10, on_value=None, off_value=None)
Y_test = tf.one_hot(Y_test, 10, on_value=None, off_value=None)

X_train = X_train.reshape([-1, 28, 28, 1])
X_test = X_test.reshape([-1, 28, 28, 1])

inputValue = k.Input(shape=(28, 28, 1))
X = k.layers.Conv2D(32, kernel_size=(5, 5), padding='same',
                    activation='relu')(inputValue)
X = k.layers.Conv2D(32, kernel_size=(
    5, 5), padding='same', activation='relu')(X)
X = k.layers.MaxPool2D(pool_size=(2, 2), strides=(1, 1))(X)
X = k.layers.Dropout(0.25)(X)
X = k.layers.Conv2D(64, kernel_size=(
    5, 5), padding='same', activation='relu')(X)
X = k.layers.Conv2D(64, kernel_size=(
    5, 5), padding='same', activation='relu')(X)
X = k.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))(X)
X = k.layers.Dropout(0.25)(X)
X = k.layers.Flatten()(X)
X = k.layers.Dense(256, activation='relu')(X)
X = k.layers.Dropout(0.5)(X)
outputValue = k.layers.Dense(10, activation='softmax')(X)
model = k.Model(inputs=inputValue, outputs=outputValue)
model.compile(optimizer='adam',
              loss=k.losses.categorical_crossentropy, metrics=['accuracy'])

model.fit(x=X_train, y=Y_train, epochs=1)

model.evaluate(X_test, Y_test)
model.save('mnist')
