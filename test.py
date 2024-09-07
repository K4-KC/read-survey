import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.Input(shape=(2000, 1000, 1)),
    keras.layers.Conv2D(filters=30, kernel_size=4, padding='same'),
    keras.layers.MaxPooling2D(pool_size=(2, 2))
])

model.compile(optimizer='rmsprop')
model.summary()