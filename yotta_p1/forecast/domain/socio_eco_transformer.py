#!/usr/bin/env python
# coding: utf-8
"""Module to transform socioeconomic features.

Classes
-------
SocioEcoTransformer

"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings as stg


class SocioEcoTransformer(BaseEstimator, TransformerMixin):
    """
    Interpolate monthly and quarterly socioeconomic features.

    Methods
    -------
    fit
    transform
    interpolate

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
        self: SocioEcoTransformer
        """

        return self

    def transform(self, X, y=None):
        """Transform method that return transformed DataFrame.

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing socioeconomic features
        y: None, default None
            Parameter not used in transformer transform method

        Returns
        -------
        X: pandas.DataFrame
        """

        # Create YEAR, MONTH, MONTH_YEAR and TRIMESTER columns
        # hypothesis: (sep, oct, nov), (dec, jan, feb)...
        X["YEAR"] = pd.DatetimeIndex(X[stg.DATE_SOCIO_COL]).year
        X["MONTH"] = pd.DatetimeIndex(X[stg.DATE_SOCIO_COL]).month
        X["MONTH_YEAR"] = pd.to_datetime(X[stg.DATE_SOCIO_COL]).dt.to_period("M")
        X = X.assign(**{"TRIMESTER" : lambda x: x.MONTH / 3 + x.YEAR * 4})

        # Interpolate monthly and quarterly features
        cls = self.__class__
        X = cls.interpolate(X, "MONTH_YEAR", stg.SOCIO_ECO_MONTH_COLS)
        X = cls.interpolate(X, "TRIMESTER", stg.SOCIO_ECO_TRIMESTER_COLS)

        # Return only features columns
        return X.filter(items=stg.SOCIO_ECO_COLS)

    @staticmethod
    def interpolate(X, key, features):
        """Static method that interpolates features according to key

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing socioeconomic features and key
        key: str
            Used to group features
        features: list
            List of features names

        Returns
        -------
        X: pandas.DataFrame
        """

        # Create grouped dataframe and interpolated features
        X_interp = X.filter(items=[key, *features])\
                    .groupby(by=key).mean()\
                    .sort_index()\
                    .interpolate()\
                    .reset_index()

        # Merge interpolated dataframe with the original one
        X_merged = X.drop(features, axis=1)\
                    .merge(right=X_interp, on=key, how="left")

        return X_merged


if __name__ == "__main__":
    socio_eco_input = "data/interim/data_socio_merged.csv"
    socio_eco_output = "data/interim/data_socio_interpolated2.csv"
    socio_eco = pd.read_csv(socio_eco_input)
    socio_eco_trans = SocioEcoTransformer().fit_transform(socio_eco)
    socio_eco_trans.to_csv(socio_eco_output, index=False)
    
    socio_eco_input = "data/raw/socio_eco.csv"
    socio_eco_output = "data/interim/socio_eco_interpolated2.csv"
    socio_eco = pd.read_csv(socio_eco_input)
    socio_eco_trans = SocioEcoTransformer().fit_transform(socio_eco)
    socio_eco_trans.to_csv(socio_eco_output, index=False)


