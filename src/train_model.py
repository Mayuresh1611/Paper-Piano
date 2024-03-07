import numpy as np
from matplotlib import pyplot as  plt
import tensorflow as tf
import os
import cv2
from  src import GLOBAL

import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout

def start_training():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    total_samples = len(os.listdir(GLOBAL.TOUCH_FOLDER) + os.listdir(GLOBAL.UNTOUCH_FOLDER))
    data = tf.keras.utils.image_dataset_from_directory("src/training_data" , image_size=(40,40), batch_size=total_samples // 5)

    data_iterator = data.as_numpy_iterator()
    batch = data_iterator.next()

    train_size = int(len(data)*.7)
    val_size = int(len(data)*.2)
    test_size = int(len(data)*.1)+1

    train = data.take(train_size)
    val = data.skip(train_size).take(val_size)
    test = data.skip(train_size+val_size).take(test_size)

    model = Sequential()

    model.add(Conv2D(32, (3,3), 1, activation='relu', input_shape=(40,40,3)))
    model.add(MaxPooling2D())

    model.add(Conv2D(16, (3,3), 1, activation='relu'))
    model.add(MaxPooling2D())

    model.add(Flatten())

    model.add(Dense(128, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))


    model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])
    print(model.summary())

    hist = model.fit(train, epochs=23, validation_data=val)

    fig = plt.figure()
    plt.plot(hist.history['loss'], color='teal', label='loss')
    plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
    fig.suptitle('Loss', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()

    fig = plt.figure()
    plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
    plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
    fig.suptitle('Accuracy', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()


    model.save('models/touch_detection_model.h5')
