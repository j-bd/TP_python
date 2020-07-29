#!/usr/bin/env python
# coding: utf-8

"""Module to parse command line.

Classes
-------
MergeCommandLineParser

"""

from argparse import ArgumentParser

from merge.settings import base


class MergeCommandLineParser:
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
            "-u", "--universe_input", help="path to universe file",
            default=base.UNIVERSE_FILE,
            )
        self.parser.add_argument(
            "-v", "--vigeo_input", help="path to vigeo file",
            default=base.VIGEO_FILE,
            )
        self.parser.add_argument(
            "-f", "--filter_input", help="path to filter file",
            default=base.ISIN_EID_FILTER_FILE,
            )

    def parse_args(self):
        """Parse main command line arguments.

        Returns
        -------
        self.parser.parse_args(): Namespace
        """
        return self.parser.parse_args()
