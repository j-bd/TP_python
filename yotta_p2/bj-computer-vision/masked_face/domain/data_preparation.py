#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import imutils
from tensorflow.keras.preprocessing.image import img_to_array

from masked_face.settings import base


class Preparation:
    """
    Apply basic transformation on images

    Attributes
    ----------

    Methods
    -------

    """
    def __init__(self, images: list):
        """

        """
        self.images = images

    def process(self):
        """
        Lauch gray, resized and normalized images steps
        Returns
        -------
        im_processed : list
            processed images in numpy array format
        """
        im_processed = []
        for im in self.images:
            image = self._gray(im)
            image = self._im_resize(image)
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
        return imutils.resize(image, width=base.WIDTH)

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
