#!/usr/bin/env python
# coding: utf-8
"""
Module to transform date.

Classes
-------
AgeTransformer

"""
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings as stg


class AgeTransformer(BaseEstimator, TransformerMixin):
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
        self: AgeTransformer
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
        if X[stg.DATA_AGE].isnull().any():
            X = self.fill_missing_value(X)

        X[stg.DATA_AGE] = X[stg.DATA_AGE].astype("category")
        X[stg.AGE_LAB]=pd.cut(
            x=X[stg.DATA_AGE], bins=stg.AGE_BINS, labels=stg.AGE_LABELS
        )

        # Return only features columns
        return X[[stg.AGE_LAB]]

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
        fill_col = df[[stg.DATA_AGE]].fillna(df[stg.DATA_AGE].mode()[0])
        return fill_col


if __name__ == "__main__":
    merged_input = "data/interim/data_socio_merged.csv"
    data_output = "data/interim/data_age.csv"
    input_df = pd.read_csv(merged_input)
    date_df = AgeTransformer().fit_transform(input_df)
    date_df.to_csv(data_output, index=False)
