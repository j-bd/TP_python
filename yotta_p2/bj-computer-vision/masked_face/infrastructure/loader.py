#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from random import shuffle

from imutils import paths


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


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
    def __init__(self, dataset_dir):
        """Class initialisation
        Parameters
        ----------
        dataset_dir : str
            directory where images are stored
        """
        self.dataset_dir = dataset_dir

    def get_raw_input(self):
        """Method to get labels and images in shuffle mode
        Returns
        -------
        raw_labels : list
            label in str format
        raw_images : list
            images are represented in numpy array format
        """
        files = self.files_listing()
        images_id = [self._get_image_id(file) for file in files]
        # Shuffle data for training purpose
        shuffle(images_id)
        labels = [self._get_label(file) for file in images_id]
        logging.info(
            f' Labels size: {len(labels)}, '
            f'Raw images size: {len(images_id)}'
        )
        return images_id, labels

    def files_listing(self):
        """Method to get all images path inside a directory
        Returns
        -------
        list of path in str format
        """
        return sorted(list(paths.list_images(self.dataset_dir)))

    def _get_label(self, file_path: str):
        """Method to have the label of an image
        Parameters
        ----------
        file_path : str
            full path of an image
        Returns
        -------
        name of label under str format
        """
        return os.path.dirname(file_path)

    def _get_image_id(self, file_path: str):
        """Method to read an image
        Parameters
        ----------
        file_path : str
            full path of an image
        Returns
        -------
        file_id : str
        """
        file_id = os.path.join(
            os.path.basename(os.path.dirname(file_path)),
            os.path.basename(file_path)
        )
        return file_id
