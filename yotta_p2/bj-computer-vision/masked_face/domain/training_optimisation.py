#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint


class TrainBySteps:

    def __init__(self, images, labels):
        self.images = images
        self.labels = labels

    def train(self):
        train_x, test_x, train_y, test_y = self._data_split()

    def _data_split(self):
        train_x, test_x, train_y, test_y = train_test_split(
            self.images, self.labels, test_size=0.20, stratify=self.labels,
            random_state=42
        )
        return train_x, test_x, train_y, test_y
