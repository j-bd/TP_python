#!/usr/bin/env python
# coding: utf-8
"""
Module to parse command line.

Classes
-------
TrainCommandLineParser
PredictCommandLineParser
"""
from argparse import ArgumentParser

from masked_face.settings import base


class TrainCommandLineParser():
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
            "-d", "--data_input", type=str, default=base.DATA_FILE,
            help="path to master input data directory"  # TODO Change with RAW_DIR at the end
        )
        self.parser.add_argument(
            "-st", "--step_training", type=bool, default=True,
            help="for hyperparameters improuvments"  # TODO Change with False at the end
        )
        self.parser.add_argument(
            "-mt", "--model_type", type=str, default=base.MODEL_CHOICE,
            help="Keras model selection"
        )
        self.parser.add_argument(
            "-dev", "--devmode", help="developper mode", type=bool,
            default=False  # TODO Change with False at the end
        )

    def parse_args(self):
        """Parse train command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return vars(self.parser.parse_args())


class PredictCommandLineParser():
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
            "-td", "--type_detection", type=str, default='image',
            help="Choice between: image / video / webcam"
        )
        self.parser.add_argument(
            "-pv", "--path_video", type=str, default=base.VIDEO_FILE,
            help="Path to your video"
        )
        self.parser.add_argument(
            "-pi", "--path_image", type=str, default=base.IMAGE_FILE,
            help="Path to your image"
        )
        self.parser.add_argument(
            "-c", "--confidence", type=float, default=0.5,
            help="Minimum probability to filter weak detections"
        )
        self.parser.add_argument(
            "-dev", "--devmode", help="developper mode", type=bool,
            default=True  # TODO put to False
        )

    def parse_args(self):
        """Parse predict command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return vars(self.parser.parse_args())
