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
    do_preprocessing
    read_csv_parquet
    sanity_check
    merge_data_socio_eco
    drop_rows_with_many_NaN
    drop_columns
    convert_target
    get_features
    get_features_target
    """

    def __init__(self, path_to_input_data, path_to_input_socio_eco,
                 target_name=stg.SUBSCRIPTION, predict=True):
        """ Initialize class (read datasets and perform sanity checks)."""
        # Set attributes
        self.path_to_input_data = path_to_input_data
        self.path_to_input_socio_eco = path_to_input_socio_eco
        self.target_name = target_name
        self.predict = predict
        # Read datasets
        self.df_data  = self.read_csv_parquet(self.path_to_input_data)
        self.df_socio = self.read_csv_parquet(self.path_to_input_socio_eco)
        # Perform sanity checks
        self.sanity_check()

    def do_preprocessing(self):
        """
        Merge dataframes and perform some preliminary treatments.
        """
        self.df_merge = self.merge_data_socio_eco()
        if not self.predict:
            self.drop_rows_with_many_NaN()
            self.convert_target()
        self.drop_columns()

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

    def sanity_check(self):
        """
        Check if expected columns are present is the datasets.
        """
        data_columns_set = set(stg.DATA_COLS)
        socio_columns_set = set([stg.DATE_DATA, *stg.SOCIO_ECO_COLS])
        if not self.predict:
            data_columns_set.add(stg.SUBSCRIPTION)
        data_diff = data_columns_set - set(self.df_data.columns)
        if len(data_diff) != 0:
           raise KeyError(data_diff, "is not present the data file")
        socio_diff = socio_columns_set - set(self.df_socio.columns)
        if len(socio_diff) != 0:
           raise KeyError(socio_diff, "is not present the socio eco file")

    def merge_data_socio_eco(self):
        """
        Merge data and socio eco input files.

        Parameters
        ----------
        path_to_file: string, default None

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
        # Return merged dataframe
        return df_merge

    def drop_rows_with_many_NaN(self):
        """
        Drop row of the dataframe with 3 NaN or more.
        """
        restriction = [stg.DATE_DATA, stg.DURATION_CONTACT, stg.RESULT_LAST_CAMPAIGN, stg.CONTACT]
        df_merge_copy = self.df_merge.drop(restriction, axis=1)
        df_merge_copy = df_merge_copy.isnull()
        nb_NaN = []
        for i in range(df_merge_copy.shape[0]):
            tmp = 0
            for j in range(df_merge_copy.shape[1]):
                if df_merge_copy.iloc[i,j] == True:
                    tmp += 1
            nb_NaN.append(tmp)
        NaN_by_row = pd.DataFrame(nb_NaN)
        NaN_by_row.columns = ['nb_NaN']
        INDEX = list(NaN_by_row.query('nb_NaN >= 3').index)
        self.df_merge = self.df_merge.drop(INDEX, axis=0)

    def drop_columns(self):
        """
        Drop some columns of the dataframe.
        """
        self.df_merge = self.df_merge.drop(columns = [stg.DURATION_CONTACT], axis=1, errors='ignore')

    def convert_target(self):
        """
        Convert the target into category.
        """
        self.df_merge[self.target_name] = self.df_merge[self.target_name].astype("category").cat.codes

    def get_features(self):
        """
        Get features from merged dataframe.

        Returns
        -------
        X: pandas.DataFrame
            Features
        """
        if self.predict:
            X = self.df_merge
        else:
            X = self.df_merge.drop(columns = [self.target_name])
        return X

    def get_features_target(self):
        """
        Get features and target from merged dataframe.

        Returns
        -------
        X, y: pandas.DataFrame, pandas.DataFrame
            Features, target
        """
        if self.predict:
            raise KeyError("There is no target to retrieve in predict mode.")
        X = self.df_merge.drop(columns = [self.target_name])
        y = self.df_merge[self.target_name]
        return X, y


if __name__ == "__main__":
    data_input = os.path.join(stg.RAW_DATA_DIR, "data.csv")
    socio_eco_input = os.path.join(stg.RAW_DATA_DIR, "socio_eco.csv")
    output = os.path.join(stg.INTERIM_DATA_DIR, "data_socio_merged.csv")
    preprocessing = Preprocessing(data_input, socio_eco_input, output)