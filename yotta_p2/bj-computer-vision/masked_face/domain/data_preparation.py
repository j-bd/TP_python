#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to realize basic transformation on raw input images and
corresponding labels. From path to image and categorical label.

Classes
-------
DataPreprocessing
ImagePreparation
LabelClassifier
"""
import logging

import cv2
import numpy as np
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.applications import vgg16
from tensorflow.keras.applications import xception
from sklearn.preprocessing import LabelEncoder

from masked_face.settings import base


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class DataPreprocessing:
    """
    Organize labels and images transformation

    Methods
    -------
    apply_preprocessing
    """
    def __init__(self, images_paths: list, labels: list, args):
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
        self.images_paths = images_paths
        self.labels = labels
        self.args = args

    def apply_preprocessing(self):
        """Call classes in charge of transforming images and labels

        Returns
        -------
        images : list
            list of numpy array
        labels_cat : list
            list of categoricalized labels
        label_classes : list
            names of labels
        """
        # Images preprocessing
        preparator = ImagePreparation(
            self.images_paths, self.args['model_type']
        )
        images = preparator.apply_basic_processing()

        # Labels Encoding
        encoder = LabelClassifier(self.labels)
        labels_cat, label_classes = encoder.get_categorical_labels()

        return images, labels_cat, label_classes


class ImagePreparation:
    """
    Apply basic transformation on images

    Methods
    -------
    apply_basic_processing
    _im_resize
    _image_scalling
    _image_padding
    _normalize
    """
    def __init__(self, images: list, model_type: str):
        """Class initialisation

        Parameters
        ----------
        images : list
            raw images in numpy array format
        model_type : str
            user choice
        """
        self.images = images
        self.model_type = model_type

    def apply_basic_processing(self):
        """
        Lauch resized and normalized images steps

        Returns
        -------
        im_processed : numpy.ndarray
            processed images in numpy array format (len(images), H, W, Channel)
        """
        im_processed = []
        for index, im in enumerate(self.images):
            image = cv2.imread(im)
            image = self._im_resize(image)
            image = img_to_array(image)
            if self.model_type == 'mobilenet_v2':
                image = mobilenet_v2.preprocess_input(image)
            elif self.model_type == 'VGG16':
                image = vgg16.preprocess_input(image)
            elif self.model_type == 'Xception':
                image = xception.preprocess_input(image)
            im_processed.append(image)

        # Set images in keras model format input: len(images), H, W, Channel
        im_processed = np.array(im_processed, dtype="float32")
        return im_processed

    def _im_resize(self, image):
        """
        Perform image resizing in format define by the users in base.py. It's
        linked with the algoritm used.
        Respect ratio for downsize and add black padding to reach defined size.

        Parameters
        ----------
        image : numpy array

        Returns
        -------
        resized_image : numpy array
            resized image in numpy array format
        """
        im_height, im_width = image.shape[:2]
        model_height, model_width = base.IMAGE_SIZE[self.model_type][:2]

        # If image is too big, downsizing is applied
        if im_height >= im_width and im_height > model_height:
            scale = round((im_height / model_height) + 0.06, 1)
            image = self._image_scalling(image, scale)
        elif im_height < im_width and im_width > model_width:
            scale = round((im_width / model_width) + 0.06, 1)
            image = self._image_scalling(image, scale)

        # if image is too small or to fit with target size, padding is applied
        im_padded = self._image_padding(image, model_height, model_width)
        resized_image = cv2.resize(im_padded, (model_height, model_width))

        return resized_image

    def _image_scalling(self, image, scale: float):
        """
        Downsize the image.

        Parameters
        ----------
        image : numpy array
        scale : float

        Returns
        -------
        resized : numpy array
            resized image in numpy array format
        """
        new_width = int(image.shape[1] / scale)
        new_height = int(image.shape[0] / scale)
        dsize = (new_width, new_height)
        resized = cv2.resize(image, dsize)
        return resized

    def _image_padding(self, image, target_h: int, target_w: int):
        """
        Add the right amount of black padding.

        Parameters
        ----------
        image : numpy array
        target_h : int
        target_w : int

        Returns
        -------
        constant : numpy array
            resized image in numpy array format
        """
        black = [0, 0, 0]
        add_line = int((target_h - image.shape[0]) / 2) + 1
        add_column = int((target_w - image.shape[1]) / 2) + 1
        constant = cv2.copyMakeBorder(
            image, add_line, add_line, add_column, add_column,
            cv2.BORDER_CONSTANT, value=black)
        return constant


class LabelClassifier:
    """
    Apply basic transformation on labels

    Methods
    -------
    get_categorical_labels
    _label_encoding
    _label_categorise
    """
    def __init__(self, labels: list):
        """Class initialisation

        Parameters
        ----------
        images : list
            labels in str format
        """
        self.labels = np.array(labels)
        self.class_nbr = len(set(self.labels))

    def get_categorical_labels(self):
        """
        Transform string label into categorised label

        Returns
        -------
        categorised_label : array
            binary class matrix
        label_classes : list
            names of the differents classes
        """
        encoded_label, label_classes = self._label_encoding()
        categorised_label = self._label_categorise(encoded_label)
        return categorised_label, label_classes

    def _label_encoding(self):
        """
        Transform str label into label with value between 0 and self.class_nbr

        Returns
        -------
        labels
            array of label under int correspondance
        label_classes : list
            names of the differents classes
        """
        self.encoder = LabelEncoder()
        labels = self.encoder.fit_transform(self.labels)
        label_classes = self.encoder.classes_
        return labels, label_classes

    def _label_categorise(self, encoded_label):
        """
        Converts a class vector to binary class matrix

        Parameters
        ----------
        encoded_label : array
            labels in int format

        Returns
        -------
            binary class matrix
        """
        return utils.to_categorical(encoded_label, self.class_nbr)
