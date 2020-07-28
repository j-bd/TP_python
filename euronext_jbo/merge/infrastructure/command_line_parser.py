#!/usr/bin/env python
# coding: utf-8

"""Module to parse command line.

Classes
-------
TrainCommandLineParser
PredictCommandLineParser

"""

from argparse import ArgumentParser

import forecast.settings as stg


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
            "-d",
            "--data_input",
            help="path to input data file",
            default=stg.DATA_FILE,
            )
        self.parser.add_argument(
            "-s",
            "--socio_eco_input",
            help="path to input socio eco file",
            default=stg.SOCIO_ECO_FILE,
            )
        self.parser.add_argument(
            "-m",
            "--model_output",
            help="path to model file output",
            default=stg.MODEL_FILE,
            )
        self.parser.add_argument(
            "-t",
            "--threshold",
            help="threshold of the prediction",
            default=.5,
            type=float
            )
        self.parser.add_argument(
            "--devmode",
            help="developper mode",
            action="store_true"
            )
        self.parser.add_argument(
            "--optimisation",
            help="Bayesian optimisation process activation",
            default=False,
            )

    def parse_args(self):
        """Parse train command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return self.parser.parse_args()


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
        """Add arguments to the parser."""
        self.parser.add_argument(
            "-d",
            "--data_input",
            help="path to input data file",
            default=stg.DATA_WITHOUT_TARGET_FILE,
            )
        self.parser.add_argument(
            "-s",
            "--socio_eco_input",
            help="path to input socio eco file",
            default=stg.SOCIO_ECO_FILE,
            )
        self.parser.add_argument(
            "-m",
            "--model_input",
            help="path to input model file",
            default=stg.MODEL_FILE,
            )
        self.parser.add_argument(
            "-p",
            "--predict_output",
            help="path to predict file output",
            default=stg.PREDICT_FILE,
            )

    def parse_args(self):
        """Parse predict command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return self.parser.parse_args()
