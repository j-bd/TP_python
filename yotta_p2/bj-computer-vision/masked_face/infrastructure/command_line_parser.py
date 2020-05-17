#!/usr/bin/env python
# coding: utf-8
"""
Module to parse command line.

Classes
-------
TrainParser
PredictParser
"""
from argparse import ArgumentParser

from masked_face.settings import base


class TrainParser():
    """Command line parser for train application.

    Methods
    -------
    parse_args
    _add_arguments
    """

    def __init__(self):
        """Initialize class."""
        self.parser = ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
        """Add arguments to the parser."""
        self.parser.add_argument(
            "-d", "--data_input", type=str, default=base.RAW_DIR,
            help="path to master input data directory"
        )
        self.parser.add_argument(
            "-st", "--step_training", type=bool, default=False,
            help="for hyperparameters improuvments"
        )
        self.parser.add_argument(
            "-mt", "--model_type", type=str, default='MobileNetV2',
            help="Keras model selection: 'MobileNetV2', 'VGG16', 'Xception'"
        )
        self.parser.add_argument(
            "-dev", "--devmode", help="developper mode", type=bool,
            default=False
        )

    def parse_args(self):
        """Parse train command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return vars(self.parser.parse_args())


class PredictParser():
    """Command line parser for predict application.

    Methods
    -------
    _add_arguments
    parse_args

    """
    def __init__(self):
        """Initialize class."""
        self.parser = ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            "-td", "--type_detection", type=str, default='webcam',
            help="Choice between: image / video / webcam"
        )
        self.parser.add_argument(
            "-pv", "--path_video", type=str,
            help="Path to your video"
        )
        self.parser.add_argument(
            "-pi", "--path_image", type=str,
            help="Path to your image"
        )
        self.parser.add_argument(
            "-ct", "--classifier_type", type=str, default='MobileNetV2',
            help="Classifier model choice: 'MobileNetV2', 'VGG16', 'Xception'"
        )
        self.parser.add_argument(
            "-c", "--confidence", type=float, default=0.5,
            help="Minimum probability to filter weak detections"
        )
        self.parser.add_argument(
            "-st", "--streamlit", type=float, default=False,
            help="Only used for API"
        )
        self.parser.add_argument(
            "-dev", "--devmode", help="developper mode", type=bool,
            default=False
        )

    def parse_args(self):
        """Parse predict command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return vars(self.parser.parse_args())
