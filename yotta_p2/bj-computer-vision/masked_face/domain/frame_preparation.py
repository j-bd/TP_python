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
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.applications import vgg16
from tensorflow.keras.applications import xception

from masked_face.settings import base


class ImagePreparation:
    """
    Apply basic transformation on images

    Methods
    -------
    apply_basic_processing
    _gray
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
            image = self._im_resize(im)
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
