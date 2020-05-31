#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to create data augmentation on the fly

Classes
-------
TrainGenerator
"""
import math

import imgaug.augmenters as iaa
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from masked_face.settings import base
from masked_face.domain.data_preparation import DataPreprocessing


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
                rotation_range=20, horizontal_flip=True,
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
                rotation_range=20, horizontal_flip=True,
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
