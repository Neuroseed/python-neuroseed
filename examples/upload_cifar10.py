import os

import numpy
import h5py
import keras
from keras.datasets import cifar10
import neuroseed

DATASET_FILE = 'cifar10.hdf5'

TOKEN = os.environ.get('AUTH_TOKEN', None) or input('Enter auth token: ')
HOST = 'http://localhost:8080'

neuroseed.authorize(TOKEN, HOST)


def cifar10_to_hdf5(file_path):
    if os.path.isfile(file_path):
        return

    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    x_train /= 255
    x_test /= 255

    x = numpy.concatenate((x_train, x_test))
    y = numpy.concatenate((y_train, y_test))

    # shuffle in-place
    numpy.random.shuffle(x)
    numpy.random.shuffle(y)

    with h5py.File(file_path, 'w') as f:
        f.create_dataset('x', data=x, compression='gzip')
        f.create_dataset('y', data=y, compression='gzip')

cifar10_to_hdf5(DATASET_FILE)

dataset = neuroseed.dataset.Dataset()
dataset.title = 'cifar10'
dataset.description = 'cifar10 dataset'
dataset.upload(DATASET_FILE)
