#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to feed pipeline with initial data

Classes
-------
Loader
"""
import os
import logging

from imutils import paths


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Loader:
    """
    Load images under numpy array and their corresponding labels.
    Label is retrieve from the name of images directory.

    Methods
    -------
    get_raw_input
    files_listing
    _get_label
    _get_raw_image
    """
    def __init__(self, dataset_dir: str):
        """Class initialisation
        Parameters
        ----------
        dataset_dir : str
            directory where images are stored
        """
        self.dataset_dir = dataset_dir

    def get_raw_input(self):
        """Method to get labels and images
        Returns
        -------
        raw_labels : list
            label in str format
        raw_images : list
            images are represented in numpy array format
        """
        paths_files = self.files_listing()
        raw_labels = [self._get_label(file) for file in paths_files]
        logging.info(
            f' Labels size: {len(raw_labels)}, '
            f'Raw images size: {len(paths_files)}'
        )
        return paths_files, raw_labels

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
        return os.path.basename(os.path.dirname(file_path))
