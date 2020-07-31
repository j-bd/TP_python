#!/usr/bin/env python
# coding: utf-8

"""
Module to save processed data.

Classes
-------
ProcessedDataSave

"""
import pandas as pd

from merge.settings import base


class ProcessedDataSave:
    """
        Save a DataFrame with vigeo keys merged values.

        Attributes
        ----------
        universe_vigeo_df: pandas.DataFrame
        saving_path: str

        Methods
        -------
        __init__
        save_file
    """
    def __init__(self, universe_vigeo_df, saving_path):
        """Initialize class"""
        self.universe_vigeo_df = universe_vigeo_df
        self.saving_path = saving_path

    def save_file(self):
        """Save final file after preprocessing and merging.
        """
        self.universe_vigeo_df.to_csv(self.saving_path)
