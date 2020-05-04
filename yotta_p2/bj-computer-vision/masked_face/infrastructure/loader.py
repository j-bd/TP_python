#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
import logging

import cv2
from imutils import paths


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


@dataclass
class Loader:
    """
    Load images under numpy array and their corresponding labels.
    Label is retrieve from the name of images directory.

    Attributes
    ----------
    dataset_dir: path of images directory in string format

    Methods
    -------
    get_raw_input
    files_listing
    get_label
    get_raw_image
    """
    dataset_dir: str

    def get_raw_input(self):
        """Method to get labels and images
        Returns
        -------
        labels: list
            label in str format
        raw_images: list
            images are represented in numpy array format
        """
        files = self.files_listing()
        labels = []
        raw_images = []
        for file in files:
            labels.append(self.get_label(file))
            raw_images.append(self.get_raw_image(file))
        return labels, raw_images

    def files_listing(self):
        """Method to get all images path inside a directory
        Returns
        -------
        list of path in str format
        """
        return sorted(list(paths.list_images(self.dataset_dir)))

    def get_label(self, file_path: str):
        """Method to have the label of an image
        Parameters
        ----------
        file_path: str
            full path of an image
        Returns
        -------
        name of label under str format
        """
        return os.path.basename(os.path.dirname(file_path))

    def get_raw_image(self, file_path: str):
        """Method to read an image
        Parameters
        ----------
        file_path: str
            full path of an image
        Returns
        -------
        numpy array
        """
        return cv2.imread(file_path)