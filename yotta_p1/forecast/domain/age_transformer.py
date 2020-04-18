#!/usr/bin/env python
# coding: utf-8
"""
Module to transform date.

Classes
-------
DateTransformer

"""
from dataclasses import dataclass

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings as stg


@dataclass
class AgeTransformer(BaseEstimator, TransformerMixin):
    """
    Process date feature.

    Methods
    -------
    fit
    transform
    fill_missing_value

    """

    df = pd.DataFrame
    y = df[stg.DATA_SUBSCRIPTION]
    X = df.drop(columns=[stg.DATA_SUBSCRIPTION])


    def fit(self):
        """Fit method that return the object itself.

        Parameters
        ----------
        X: pandas.DataFrame
            Parameter not used in transformer fit method
        y: None, default None
            Parameter not used in transformer fit method

        Returns
        -------
        self: AgeTransformer
        """
        return self

    def transform(self):
        """Transform method that return transformed DataFrame.

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing full features
        y: None, default None
            Parameter not used in transformer transform method

        Returns
        -------
        X: pandas.DataFrame
        """
        if self.X[stg.DATA_DATE].isnull().any():
            self.X = self.fill_missing_value(self.X)

        self.X['DATE'] = pd.to_datetime(self.X['DATE'], format=stg.DATA_DATE_FORMAT)
        self.X["day"] = self.X['DATE'].dt.day #remove ?
        self.X["year"] = self.X['DATE'].dt.year #remove ?
        self.X["weekday"] = self.X['DATE'].dt.day_name()
        self.X["month"] = self.X['DATE'].dt.month_name()

        self.X["day_selected"] = self.X["weekday"].apply(
            lambda x: 0 if x in stg.WEEKEND else 1
        )
        self.X["hot_month"] = self.X["month"].apply(
            lambda x: 1 if x in stg.HOT_MONTH else 0
        )
        self.X["warm_month"] = self.X["month"].apply(
            lambda x: 1 if x in stg.WARM_MONTH else 0
        )
        self.X["cold_month"] = self.X["month"].apply(
            lambda x: 1 if x in stg.COLD_MONTH else 0
        )
        # Return only features columns
        return self.X.filter(items=stg.DATE_COLS)

    def fill_missing_value(self, df):
        """Transform method that return transformed DataFrame.

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing full features
        y: None, default None
            Parameter not used in transformer transform method

        Returns
        -------
        X: pandas.DataFrame
        """
        return df.fillna(method='ffill', inplace=True)


if __name__ == "__main__":
    merged_input = "data/interim/data_socio_merged.csv"
    data_output = "data/interim/data_age.csv"
    input_df = pd.read_csv(merged_input)
    date_df = AgeTransformer().fit_transform(input_df)
    date_df.to_csv(data_output, index=False)
