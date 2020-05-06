#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import imutils
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.image import img_to_array

from masked_face.settings import base


class ImagePreparation:
    """
    Apply basic transformation on images

    Attributes
    ----------
    images : raw images

    Methods
    -------
    process
    _gray
    _im_resize
    _normalize
    """
    def __init__(self, images: list, model: str, debug=False):
        """Class initialisation
        Parameters
        ----------
        images : list
            images in numpy array format
        """
        self.images = images
        self.model = model
        self.debug = debug

    def apply_basic_processing(self):
        """
        Lauch gray, resized and normalized images steps
        Returns
        -------
        im_processed : list
            processed images in numpy array format
        """
        im_processed = []
        for index, im in enumerate(self.images):
            image = self._im_resize(im)
            if self.debug:
                show_each = 200
                if index % show_each == 0:
                    cv2.imshow('image_check', image)
                    cv2.waitKey()
            image = img_to_array(image)
            image = self._normalize(image)
            im_processed.append(image)
        return im_processed

    def _gray(self, image):
        """
        Return the gray value of an color image
        Parameters
        ----------
        image : numpy array
            bgr style
        Returns
        -------
            gray style image in numpy array format
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _im_resize(self, image):
        """
        Return input image in format define by the users in base.py. It's
        linked with the algoritm used
        Parameters
        ----------
        image : numpy array
        Returns
        -------
            resized image in numpy array format
        """
        im_height, im_width = image.shape[:2]
        model_height, model_width = base.IMAGE_SIZE[self.model][:2]

        if im_height >= im_width and im_height > model_height:
            scale = round((im_height / model_height) + 0.06, 1)
            image = self._image_scalling(image, scale)
        elif im_height < im_width and im_width > model_width:
            scale = round((im_width / model_width) + 0.06, 1)
            image = self._image_scalling(image, scale)

        im_padded = self._image_padding(image, model_height, model_width)
        resized_image = cv2.resize(im_padded, (model_height, model_width))

        return resized_image

    def _image_scalling(self, image, scale):
        new_width = int(image.shape[1] / scale)
        new_height = int(image.shape[0] / scale)
        dsize = (new_width, new_height)
        resized = cv2.resize(image, dsize)
        return resized

    def _image_padding(self, image, target_h, target_w):
        black = [0, 0, 0]
        add_line = int((target_h - image.shape[0]) / 2) + 1
        add_column = int((target_w - image.shape[1]) / 2) + 1
        constant = cv2.copyMakeBorder(
            image, add_line, add_line, add_column, add_column,
            cv2.BORDER_CONSTANT, value=black)
        return constant

    def _normalize(self, image):
        """
        Return a normalize image from range 0-255 to range 0-1
        Parameters
        ----------
        image : numpy array
        Returns
        -------
            normalized image in numpy array format
        """
        return np.array(image, dtype="float") / 255.0


class LabelClassifier:
    """
    Apply basic transformation on labels

    Attributes
    ----------
    labels : list

    Methods
    -------

    """
    def __init__(self, labels: list):
        """Class initialisation
        Parameters
        ----------
        images : list
            labels in str format
        """
        self.labels = labels
        self.class_nbr = len(set(self.labels))

    def process(self):
        """
        Transform string label into categorised label
        Returns
        -------
        categorised_label : array
            binary class matrix
        """
        encoded_label = self._label_encoding()
        categorised_label = self._label_categorise(encoded_label)
        return categorised_label

    def _label_encoding(self):
        """
        Transform str label into label with value between 0 and self.class_nbr
        Returns
        -------
            array of label under int correspondance
        """
        self.encoder = LabelEncoder()
        return self.encoder.fit_transform(self.labels)

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
