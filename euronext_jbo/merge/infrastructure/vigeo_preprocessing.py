#!/usr/bin/env python
# coding: utf-8

"""
Module to preprocess raw data.

Classes
-------
VigeoPreprocessing

"""

import os

import pandas as pd

from merge.settings import base


class VigeoPreprocessing:
    """
        Return a DataFrame with some pretreatments performing.

        Attributes
        ----------
        vigeo_data_path: str

        Methods
        -------
        __init__
        do_preprocessing
        read_csv
        sanity_check
        cast_columns
    """
    def __init__(self, vigeo_data_path):
        """Initialize class"""
        self.vigeo_data_path = vigeo_data_path

    def do_preprocessing(self):
        """Perform some preliminary treatments.

        Returns
        -------
        vigeo_df: pandas.DataFrame
        """
        vigeo_df = self.read_csv()
        self.sanity_check(vigeo_df)
        vigeo_df = self.cast_columns(vigeo_df)
        return vigeo_df

    def read_csv(self):
        """
        Create dataframe from input csv file.

        Returns
        -------
        pandas.DataFrame
        """
        # File name and extension
        file_name, file_extension = os.path.splitext(self.vigeo_data_path)
        # Read input file
        if file_extension == ".xlsx":
            return pd.read_csv(self.vigeo_data_path)
        else:
            raise TypeError(
                f"The file format {file_extension} is not treated."
            )

    def sanity_check(self, df):
        """
        Check if expected columns are present is the dataset.
        """
        data_columns_set = set(base.V_COLUMNS)
        data_diff = data_columns_set - set(df.columns)
        if len(data_diff) != 0:
            raise KeyError(data_diff, "is not present in the vigeo file")

    def cast_columns(self, df):
        """
        Cast dataframe columns as expected.

        Returns
        -------
        pandas.DataFrame
        """
        return df.astype(base.V_COLUMNS_CAST)
