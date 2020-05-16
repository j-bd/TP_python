#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to realize a training with validation dataset (steps) or with all the
data (full)

Classes
-------
StepsRun
FullRun
"""

import logging
import random

from sklearn.model_selection import train_test_split

from masked_face.settings import base
from masked_face.infrastructure.model_creation import ModelConstructor
from masked_face.infrastructure.model_creation import CallbacksConstructor
from masked_face.domain.data_preparation import DataPreprocessing
from masked_face.domain.data_augmentation import TrainGenerator


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class StepsRun:
    """
    Operate training with a validation dataset

    Methods
    -------
    launching_steps
    """
    def __init__(self, paths_images: list, labels: list, args):
        """Class initialisation

        Parameters
        ----------
        paths_images : list
            list of paths to selected images
        labels : list
            list of labels (str) corresponding to the images paths
        args : arguments parser
            list of user arguments
        """
        self.paths_images = paths_images
        self.labels = labels
        self.args = args

    def launching_steps(self):
        """Process data split and preprocess before launching training

        Returns
        -------
        model : keras model
            trained model
        history : dict
            training history
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
        callbacks_creator = CallbacksConstructor(self.args['model_type'])
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
    Operate training with the full dataset

    Methods
    -------
    launching_steps
    """
    def __init__(self, paths_images: list, labels: list, args):
        """Class initialisation

        Parameters
        ----------
        paths_images : list
            list of paths to selected images
        labels : list
            list of labels (str) corresponding to the images paths
        args : arguments parser
            list of user arguments
        """
        self.paths_images = paths_images
        self.labels = labels
        self.args = args

    def launching_steps(self):
        """Preprocess data before launching training

        Returns
        -------
        model : keras model
            trained model
        history : dict
            training history
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
