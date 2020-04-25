#!/usr/bin/env python
# coding: utf-8
"""
Module to transform date.

Classes
-------
BankStatus_Transformer

"""
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings as stg


class BankStatusTransformer(BaseEstimator, TransformerMixin):
    """
    Process date feature.

    Methods
    -------
    fit
    transform
    fill_missing_value

    """

    def fit(self, X, y=None):
        """Fit method that return the object itself.

        Parameters
        ----------
        X: pandas.DataFrame
            Parameter not used in transformer fit method
        y: None, default None
            Parameter not used in transformer fit method

        Returns
        -------
        self: BankStatusTransformer
        """
        return self

    def transform(self, X, y=None):
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
        for column in stg.BANK_STATUS_COL:
            if X[column].isnull().any():
                X[column] = self.fill_missing_value(X, column)

            X[column] = X[column].astype("category")
            X[column] = X[column].cat.codes

        X[stg.BANK_STATUS_LAB] = X[stg.BANK_STATUS_COL].sum(axis=1)
        X[stg.BANK_STATUS_LAB] = (X[stg.BANK_STATUS_LAB] - 3).abs()

        # Return only features columns
        return X[[stg.BANK_STATUS_LAB]]

    def get_feature_names(self):
        return [stg.BANK_STATUS_LAB]

    def fill_missing_value(self, df, column):
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
        fill_col = df.fillna(df[column].mode()[0])
        return fill_col


if __name__ == "__main__":
    merged_input = "data/interim/data_socio_merged.csv"
    data_output = "data/interim/data_age.csv"
    input_df = pd.read_csv(merged_input)
    date_df = BankStatusTransformer().fit_transform(input_df)
    date_df.to_csv(data_output, index=False)
