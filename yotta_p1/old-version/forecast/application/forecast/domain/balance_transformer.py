#!/usr/bin/env python
# coding: utf-8
"""Module to transform balance feature.

Classes
-------
BalanceTransformer

"""

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

import forecast.settings as stg


class BalanceTransformer(BaseEstimator, TransformerMixin):
    """
    ...

    Methods
    -------
    fit
    transform

    """

    def __init__(self, var_type):

        self.var_type = var_type

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

        cls = self.__class__
        if self.var_type == "cat":
            cls.add_AT_DEBIT(X)
            cls.add_PRECARITY(X)
            return X[['AT_DEBIT', 'PRECARITY']]
        if self.var_type == "num":
            cls.treat_BALANCE(X)
            return X[[stg.BALANCE]]

    def get_feature_names(self):
        if self.var_type == "cat":
            return ['AT_DEBIT', 'PRECARITY']
        if self.var_type == "num":
            return [stg.BALANCE]

    @staticmethod
    def add_AT_DEBIT(X):
        X['AT_DEBIT'] = 'No'
        AT_DEBIT_TRUE = X.query('{} < 0'.format(stg.BALANCE))\
                         .assign(AT_DEBIT=lambda x: 'Yes').copy()
        INDEX = list(X.query('{} < 0'.format(stg.BALANCE)).index)
        X.loc[INDEX] = AT_DEBIT_TRUE

    @staticmethod
    def add_PRECARITY(X):
        X['PRECARITY'] = 'No' 
        PRECARITY_TRUE = X.query('{} ==0 '.format(stg.BALANCE))\
                                    .assign(PRECARITY=lambda x: 'Yes').copy()
        INDEX = list(X.query('{} ==0 '.format(stg.BALANCE)).index)
        X.loc[INDEX] = PRECARITY_TRUE

    @staticmethod
    def treat_BALANCE(X):
        X[stg.BALANCE] = X[stg.BALANCE].apply(lambda x: np.absolute(x)).copy()
        INDEX_DEBIT = list(X.query('{} >= 0 and {} < 1'.format(stg.BALANCE,stg.BALANCE)).index)
        X.loc[INDEX_DEBIT,stg.BALANCE] = 1
        X[stg.BALANCE] = X[stg.BALANCE].apply(lambda x: np.log(x)).copy()

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


