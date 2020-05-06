#!/usr/bin/env python
# coding: utf-8

"""Module to parse command line.

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

    """

    def __init__(self):
        """Initialize class."""
        self.parser = ArgumentParser()
        self._add_arguments()

    def _add_arguments(self):
        """Add arguments to the parser."""
        self.parser.add_argument(
            "-d", "--data_input", help="path to input data",
            default=base.DATA_FILE
        )
        self.parser.add_argument(
            "-m", "--model_output", help="path to model file output",
            default=base.MODEL_FILE
        )
        self.parser.add_argument(
            "-st", "--step_training", help="for hyperparameters improvments",
            default=True
        )
        self.parser.add_argument(
            "-mt", "--model_type", help="Keras model selection",
            default=base.MODEL_CHOICE
        )
        self.parser.add_argument(
            "-dev", "--devmode", help="developper mode", default=True
        )

    def parse_args(self):
        """Parse train command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return vars(self.parser.parse_args())


#class PredictCommandLineParser():
#    """Command line parser for predict application.
#
#    Methods
#    -------
#    parse_args
#
#    """
#
#    def __init__(self):
#        """Initialize class."""
#        self.parser = ArgumentParser()
#        self._add_arguments()
#
#    def _add_arguments(self):
#        """Add arguments to the parser."""
#        self.parser.add_argument(
#            "-d",
#            "--data_input",
#            help="path to input data file",
#            default=stg.DATA_WITHOUT_TARGET_FILE,
#            )
#        self.parser.add_argument(
#            "-s",
#            "--socio_eco_input",
#            help="path to input socio eco file",
#            default=stg.SOCIO_ECO_FILE,
#            )
#        self.parser.add_argument(
#            "-m",
#            "--model_input",
#            help="path to input model file",
#            default=stg.MODEL_FILE,
#            )
#        self.parser.add_argument(
#            "-p",
#            "--predict_output",
#            help="path to predict file output",
#            default=stg.PREDICT_FILE,
#            )
#
#    def parse_args(self):
#        """Parse predict command line arguments.
#
#        Returns
#        -------
#        self.parser.parse_args(): Namespace
#        """
#        return self.parser.parse_args()
