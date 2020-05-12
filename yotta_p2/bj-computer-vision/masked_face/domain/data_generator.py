#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import numpy as np
import keras
import cv2
from sklearn.preprocessing import LabelEncoder

from masked_face.settings import base


class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, images_id, labels, batch_size, dim, n_classes,
                 shuffle=True, directory):
        'Initialization'
        self.images_id = images_id
        self.labels = labels
        self.batch_size = batch_size
        self.dim = dim[:2]
        self.n_channels = dim[-1]
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.directory = directory
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.images_id) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        images_id_temp = [self.images_id[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(images_id_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.images_id))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, images_id_temp):
        'Generates data containing batch_size samples'  # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, self.dim, self.n_channels))  # TODO *removed
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for idx, im_id in enumerate(images_id_temp):
            # Store sample
            X[idx, ] = cv2.imread(os.path.join(self.directory, im_id))  # TODO + ID + '.npy'

            # Store class
            y[idx] = self.labels[im_id]

        self.encoder = LabelEncoder()
        y = self.encoder.fit_transform(self.labels)

        return X, y
