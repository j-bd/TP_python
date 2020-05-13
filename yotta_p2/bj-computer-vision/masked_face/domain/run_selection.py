#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:17:22 2020

@author: j-bd
"""
import math
import logging
import random

from tensorflow.keras.utils import Sequence
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from masked_face.settings import base
from masked_face.infrastructure.model_creation import ModelConstructor, CallbacksConstructor
from masked_face.domain.data_preparation import DataPreprocessing


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class StepsRun:
    """
    """
    def __init__(self, paths_images, labels, args):
        """
        """
        self.paths_images = paths_images
        self.labels = labels
        self.args = args

    def launching_steps(self):
        """
        """
        self.train_x, self.val_x, self.train_y, self.val_y = train_test_split(
            self.paths_images, self.labels, test_size=0.10, random_state=42
        )

        # Validation data preparation
        preprocess = DataPreprocessing(self.val_x, self.val_y, self.args)
        self.val_x, self.val_y, label_cl = preprocess.apply_preprocessing()

        # Generator for train data
        batch_im_generator = TrainGenerator(
            self.train_x, self.train_y, 32, self.args
        )

        # Model instanciation
        logging.info(' Model infrastructure construction ...')
        model_creator = ModelConstructor(self.args['model_type'])
        model = model_creator.get_model()

        # Callbacks creation
        logging.info(' Callbacks calling ...')
        callbacks_creator = CallbacksConstructor()
        callbacks = callbacks_creator.get_callbacks()

        # Launch model training
        logging.info(' Training model ...')
        history = model.fit(
            batch_im_generator, epochs=base.EPOCHS,
            validation_data=(self.val_x, self.val_y), callbacks=callbacks
        )
        return model, history


class FullRun:
    """
    """
    def __init__(self, paths_images, labels, args):
        """
        """
        self.paths_images = paths_images
        self.labels = labels
        self.args = args

    def launching_steps(self):
        """
        """
        full_data = list(zip(self.paths_images, self.labels))
        random.shuffle(full_data)
        self.paths_images, self.labels = zip(*full_data)

        # Generator for train data
        batch_im_generator = TrainGenerator(
            self.paths_images, self.labels, 32, self.args
        )

        # Model instanciation
        logging.info(' Model infrastructure construction ...')
        model_creator = ModelConstructor(self.args['model_type'])
        model = model_creator.get_model()

        # Callbacks creation
        logging.info(' Callbacks calling ...')
        callbacks_creator = CallbacksConstructor()
        callbacks = callbacks_creator.get_callbacks()

        # Launch model training
        logging.info(' Training model ...')
        history = model.fit(
            x=batch_im_generator, epochs=base.EPOCHS, callbacks=callbacks
        )
        return model, history


class TrainGenerator(Sequence):

    def __init__(self, x_set, y_set, batch_size, args):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size
        self.args = args

    def __len__(self):
        return math.ceil(len(self.x) / self.batch_size)

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]

        preprocess = DataPreprocessing(batch_x, batch_y, self.args)
        train_x, train_y, label_cl = preprocess.apply_preprocessing()

        if self.args['devmode']:
            datagen = ImageDataGenerator(
                featurewise_center=True, featurewise_std_normalization=True,
                rotation_range=45, horizontal_flip=True,
                brightness_range=[0.2, 1.0]
            )
            datagen.fit(train_x)
            gen = next(datagen.flow(
                train_x, train_y, batch_size=32,
                save_to_dir=base.IMAGE_GENERATOR, save_prefix='aug',
                save_format='png')
            )
        else:
            datagen = ImageDataGenerator(
                featurewise_center=True, featurewise_std_normalization=True,
                rotation_range=45, horizontal_flip=True,
                brightness_range=[0.2, 1.0]
            )
            datagen.fit(train_x)
            gen = next(datagen.flow(train_x, train_y, batch_size=32))

        return gen
