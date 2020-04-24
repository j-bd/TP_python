#!/usr/bin/env python
# coding: utf-8
"""
Module to transform date.

Classes
-------
DateTransformer

"""
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings as stg


class DateTransformer(BaseEstimator, TransformerMixin):
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
        self: DateTransformer
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
        if X[stg.DATE_DATA].isnull().any():
            X = self.fill_missing_value(X)

        X[stg.DATE_DATA] = pd.to_datetime(X[stg.DATE_DATA], format=stg.DATA_DATE_FORMAT)
        X[stg.DAY_SELECTED_COL] = X[stg.DATE_DATA].dt.day_name()
        X[stg.MONTH_LAB] = X[stg.DATE_DATA].dt.month_name()

        X[stg.DAY_SELECTED_COL] = X[stg.DAY_SELECTED_COL].apply(
            lambda x: 0 if x in stg.WEEKEND else 1
        )
#        X[stg.HOT_MONTH_COL] = X["month"].apply(
#            lambda x: 1 if x in stg.HOT_MONTH else 0
#        )
#        X[stg.WARM_MONTH_COL] = X["month"].apply(
#            lambda x: 1 if x in stg.WARM_MONTH else 0
#        )
#        X[stg.COLD_MONTH_COL] = X["month"].apply(
#            lambda x: 1 if x in stg.COLD_MONTH else 0
#        )
        X[stg.MONTH_LAB] = X[stg.MONTH_LAB].replace(stg.MONTH_ENCODING)

        # Return only features columns
        return X[stg.DATE_COLS]

    def get_feature_names(self):
        return stg.DATE_COLS

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
        fill_col = df[[stg.DATE_DATA]].fillna(method='ffill')
        return fill_col


if __name__ == "__main__":
    merged_input = "data/interim/data_socio_merged.csv"
    data_output = "data/interim/data_date.csv"
    input_df = pd.read_csv(merged_input)
    date_df = DateTransformer().fit_transform(input_df)
    date_df.to_csv(data_output, index=False)
