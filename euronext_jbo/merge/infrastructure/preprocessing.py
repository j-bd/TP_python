#!/usr/bin/env python
# coding: utf-8

"""
Module to preprocess raw data.

Classes
-------
UniversePreprocessing

"""

import os

import pandas as pd

from merge.settings import base


class UniversePreprocessing:
    """
        Return a DataFrame with some pretreatments performing.

        Attributes
        ----------
        universe_df: pandas.DataFrame
        universe_data_path: str

        Methods
        -------
        __init__
    """
    def __init__(self, universe_data_path):
        """Initialize class"""
        self.universe_data_path = universe_data_path

    def do_preprocessing(self):
        """Perform some preliminary treatments.

        Returns
        -------
        pandas.DataFrame
        """
        universe_df = self.read_csv()
        self.sanity_check()
        universe_df = self.cast_columns(universe_df)

    def read_csv(self):
        """
        Create dataframe from input csv file.

        Returns
        -------
        pandas.DataFrame
        """
        # File name and extension
        file_name, file_extension = os.path.splitext(self.universe_data_path)
        # Read input file
        if file_extension == ".csv":
            return pd.read_csv(self.universe_data_path)
        else:
            raise TypeError(
                f"The file format {file_extension} is not treated."
            )

    def sanity_check(self):
        """
        Check if expected columns are present is the datasets.
        """
        data_columns_set = set(base.U_COLUMNS)
        data_diff = data_columns_set - set(self.universe_df.columns)
        if len(data_diff) != 0:
            raise KeyError(data_diff, "is not present in the universe file")

    def cast_columns(self, df):
        """
        Cast dataframe columns as expected.

        Returns
        -------
        pandas.DataFrame
        """
        return df.astype(base.U_COLUMNS_CAST).dtypes
