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
            default=True  # TODO Change with False at the end
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
    parse_args

    """
    def __init__(self):
        """Initialize class."""
        self.parser = ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
#        self.parser.add_argument(
#            "-d", "--data_input", type=str, default=base.,
#            help="path to master input data directory"  # TODO Change with RAW_DIR at the end
#        )
        self.parser.add_argument(
            "-td", "--type_detection", type=str, default='webcam',
            help="Choice between: image / video / webcam"
        )
        self.parser.add_argument(
            "-fd", "--face_detection", type=str, default=base.MODEL_DETECTION,
            help="Path to face detection model"
        )
        self.parser.add_argument(
            "-fc", "--face_classification", type=str, default=base.MODEL_FILE,
            help="Path to face classification model"
        )
        self.parser.add_argument(
            "-c", "--confidence", type=float, default=0.5,
            help="Minimum probability to filter weak detections")
#        self.parser.add_argument(
#            "-dev", "--devmode", help="developper mode", type=bool,
#            default=True  # TODO Change with False at the end
#        )
        self.parser.add_argument(
            "-p", "--predict_output", type=str, default=base.OUTPUT_DIR,
            help="Path to predict file output"
        )

    def parse_args(self):
        """Parse predict command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return self.parser.parse_args()
