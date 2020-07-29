#!/usr/bin/env python
# coding: utf-8

"""
Module to preprocess raw data.

Classes
-------
IsinEidPreprocessing

"""

import os

import pandas as pd

from merge.settings import base


class IsinEidPreprocessing:
    """
        Return a DataFrame with some pretreatments performing.

        Attributes
        ----------
        isin_eid_data_path: str

        Methods
        -------
        __init__
        do_preprocessing
        read_csv
        sanity_check
        cast_columns
    """
    def __init__(self, isin_eid_data_path):
        """Initialize class"""
        self.isin_eid_data_path = isin_eid_data_path

    def do_preprocessing(self):
        """Perform some preliminary treatments.

        Returns
        -------
        universe_df: pandas.DataFrame
        """
        isin_eid_df = self.read_csv()
        self.sanity_check(isin_eid_df)
        isin_eid_df = self.cast_columns(isin_eid_df)
        return isin_eid_df

    def read_csv(self):
        """
        Create dataframe from input csv file.

        Returns
        -------
        pandas.DataFrame
        """
        # File name and extension
        file_name, file_extension = os.path.splitext(self.isin_eid_data_path)
        # Read input file
        if file_extension == ".csv":
            return pd.read_csv(self.isin_eid_data_path)
        else:
            raise TypeError(
                f"The file format {file_extension} is not treated."
            )

    def sanity_check(self, df):
        """
        Check if expected columns are present is the dataset.
        """
        data_columns_set = set(base.F_COLUMNS)
        data_diff = data_columns_set - set(df.columns)
        if len(data_diff) != 0:
            raise KeyError(data_diff, "is not present in the universe file")

    def cast_columns(self, df):
        """
        Cast dataframe columns as expected.

        Returns
        -------
        pandas.DataFrame
        """
        return df.astype(base.F_COLUMNS_CAST)
