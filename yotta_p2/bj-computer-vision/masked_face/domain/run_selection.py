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
import math
import logging
import random

from sklearn.model_selection import train_test_split
import imgaug.augmenters as iaa
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from masked_face.settings import base
from masked_face.infrastructure.model_creation import ModelConstructor
from masked_face.infrastructure.model_creation import CallbacksConstructor
from masked_face.domain.data_preparation import DataPreprocessing


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


class TrainGenerator(Sequence):
    """
    TrainGenerator inherits from keras.utils.Sequence. Methods __len__ and
    __getitem__ are mandatory.
    Select batch of path images before preprocessing them. It also add data
    augmentation

    Warning: in 'devmod', augmented images will be stored. The size will
    rqpidly increase. A great advice: chosoe a short set of images. You will
    find those images in logs/image_data_generator directory.

    Methods
    -------
    additional_augmentation
    """
    def __init__(self, x_set: list, y_set: list, batch_size: int, args):
        """Class initialisation

        Parameters
        ----------
        x_set : list
            list of paths to selected images
        y_set : list
            list of labels (str) corresponding to the images paths
        batch_size : int
            numbers of images process together
        args : arguments parser
            list of user arguments
        """
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

        # Caution when launching this mode. Select a small dataset (ie 20)
        if self.args['devmode']:
            datagen = ImageDataGenerator(
                featurewise_center=True, featurewise_std_normalization=True,
                rotation_range=45, horizontal_flip=True,
                brightness_range=[0.2, 1.0],
                preprocessing_function=self.additional_augmentation
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
                brightness_range=[0.2, 1.0],
                preprocessing_function=self.additional_augmentation
            )
            datagen.fit(train_x)
            gen = next(datagen.flow(train_x, train_y, batch_size=32))
        return gen

    def additional_augmentation(self, image):
        """Apply two augmentations on the same image

        Parameters
        ----------
        image : numpy array
            image to be augmented

        Returns
        -------
        image : numpy array
            image augmented
        """
        aug1 = iaa.GaussianBlur(sigma=(0, 2.0))
        aug2 = iaa.AdditiveGaussianNoise(scale=0.01 * 255)
        image = aug1.augment_image(image)
        image = aug2.augment_image(image)
        return image
