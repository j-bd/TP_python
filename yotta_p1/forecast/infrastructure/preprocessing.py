#!/usr/bin/env python
# coding: utf-8
"""Module to preprocess raw data.

Classes
-------
Preprocessing

"""

import os
import pandas as pd

import forecast.settings as stg

class Preprocessing:
    """
    Create a DataFrame with two given csv files and perform some pretreatments.

    Attributes
    ----------
    df_data: pandas.DataFrame
    df_socio: pandas.DataFrame
    df_merged: pandas.DataFrame
    target_name: str

    Methods
    -------
    __init__
    read_csv_parquet
    merge_data_socio_eco
    drop_columns
    convert_target
    get_features_target
    """

    def __init__(self, path_to_input_data, path_to_input_socio_eco, path_to_output,
                 save_output=True, target_name=stg.SUBSCRIPTION):
        """ Initialize class.

        Create data and socio eco dataframes from corresponding input files and merge them.

        Parameters
        ----------
        path_to_input_data: string
        path_to_input_socio_eco: string
        path_to_output: string
        save_output: bool, default True
        target_name: str, default stg.SUBSCRIPTION
        """
        self.df_data  = self.read_csv_parquet(path_to_input_data)
        self.df_socio = self.read_csv_parquet(path_to_input_socio_eco)
        self.df_merge = self.merge_data_socio_eco(path_to_output, save_output)
        self.target_name = target_name
        self.drop_columns([stg.DURATION_CONTACT])
        self.convert_target()

    @staticmethod
    def read_csv_parquet(path_to_file):
        """
        Create dataframe from input csv or parquet file.

        Parameters
        ----------
        path_to_file: string

        Returns
        -------
        pandas.DataFrame
        """
        # File name and extension
        file_name, file_extension = os.path.splitext(path_to_file)
        # Read input file
        if file_extension == ".csv":
            return pd.read_csv(path_to_file)
        elif file_extension == ".parquet":
            return pd.read_parquet(path_to_file)
        else:
            raise TypeError(f"The file format {file_extension} is not treated.")

    def merge_data_socio_eco(self, path_to_output, save_output=True):
        """
        Merge data and socio eco input files.

        Parameters
        ----------
        path_to_file: string
        save_output: bool, default True

        Returns
        -------
        pandas.DataFrame
        """
        # Create temporary month_year key columns
        self.df_data["MONTH_YEAR"]  = pd.to_datetime(self.df_data[stg.DATE_DATA]).dt.to_period("M")
        self.df_socio["MONTH_YEAR"] = pd.to_datetime(self.df_socio[stg.DATE_SOCIO_COL]).dt.to_period("M")
        # Merge socio eco dataframe with data according to month_year
        df_merge = self.df_data.merge(right=self.df_socio.drop(columns=[stg.DATE_SOCIO_COL]), on="MONTH_YEAR", how="left")\
                               .drop(columns=["MONTH_YEAR"])
        # Save merged dataframe
        if save_output:
            df_merge.to_csv(path_to_output, index=False)
        # Return merged dataframe
        return df_merge

    def drop_columns(self, columns):
        """
        Drop columns of the dataframe.

        Parameters
        ----------
        columns: list
            Columns to drop
        """
        self.df_merge = self.df_merge.drop(columns = columns)

    def convert_target(self):
        """
        Convert the target into category.
        """
        self.df_merge[self.target_name] = self.df_merge[self.target_name].astype("category").cat.codes

    def get_features_target(self):
        """
        Get features and target from merged dataframe.

        Returns
        -------
        X, y: pandas.DataFrame, pandas.DataFrame
            Features, target
        """
        X = self.df_merge.drop(columns = [self.target_name])
        y = self.df_merge[self.target_name]
        return X, y


if __name__ == "__main__":
    data_input = os.path.join(stg.RAW_DATA_DIR, "data.csv")
    socio_eco_input = os.path.join(stg.RAW_DATA_DIR, "socio_eco.csv")
    output = os.path.join(stg.INTERIM_DATA_DIR, "data_socio_merged.csv")
    preprocessing = Preprocessing(data_input, socio_eco_input, output)