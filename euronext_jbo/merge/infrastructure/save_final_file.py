#!/usr/bin/env python
# coding: utf-8

"""
Module to save processed data.

Classes
-------
ProcessedDataSave

"""
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
        # Clean unuseful column
        self._drop_column()
        # Data saving
        self.universe_vigeo_df.to_csv(self.saving_path)

    def _drop_column(self):
        """Suppress working column"""
        self.universe_vigeo_df.drop(columns=[base.DATE], inplace=True)
