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
    Add new columns related to the BALANCE and treat BALANCE.
    Methods
    -------
    fit
    transform
    get_feature_names
    add_AT_DEBIT
    add_PRECARITY
    treat_BALANCE
    """

    def __init__(self, var_type):
        """Initialize class."""

        self.var_type = var_type

    def fit(self, X, y=None):
        """
        Fit method that return the object itself.

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
        """
        Transform method that return transformed DataFrame.

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
            return X[stg.BALANCE_CAT_COLS]
        if self.var_type == "num":
            X_copy = cls.treat_BALANCE(X)
            return X_copy

    def get_feature_names(self):
        if self.var_type == "cat":
            return stg.BALANCE_CAT_COLS # , stg.PRECARITY
        if self.var_type == "num":
            return [stg.BALANCE]

    @staticmethod
    def add_AT_DEBIT(X):
        """
        Create a column at debit.

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing BALANCE features.

        Returns
        -------
        """
        X[stg.AT_DEBIT] = 'No'
        AT_DEBIT_TRUE = X.query('{} < 0'.format(stg.BALANCE))\
                         .assign(AT_DEBIT=lambda x: 'Yes').copy()
        INDEX = list(X.query('{} < 0'.format(stg.BALANCE)).index)
        X.loc[INDEX] = AT_DEBIT_TRUE

    @staticmethod
    def add_PRECARITY(X):
        """
        Create a column precarity.

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing BALANCE features.

        Returns
        -------
        """
        X[stg.PRECARITY] = 'No' 
        PRECARITY_TRUE = X.query('{} ==0 '.format(stg.BALANCE))\
                                    .assign(PRECARITY=lambda x: 'Yes').copy()
        INDEX = list(X.query('{} ==0 '.format(stg.BALANCE)).index)
        X.loc[INDEX] = PRECARITY_TRUE

    @staticmethod
    def treat_BALANCE(X):
        """
        Treat BALANCE features.

        Parameters
        ----------
        X: pandas.DataFrame
            DataFrame containing BALANCE features.

        Returns
        -------
        """
        # X[stg.BALANCE] = X[stg.BALANCE].apply(lambda x: np.absolute(x)).copy()
        # INDEX_DEBIT = list(X.query('{} >= 0 and {} < 1'.format(stg.BALANCE,stg.BALANCE)).index)
        # X.loc[INDEX_DEBIT,stg.BALANCE] = 1
        # X[stg.BALANCE] = X[stg.BALANCE].apply(lambda x: np.log(x)).copy()
        X_copy = X.copy()
        UPPERBOUND, LOWERBOUND = np.percentile(X_copy[stg.BALANCE], [0.25, 99.75]) 
        X_copy = np.clip(X_copy[stg.BALANCE], UPPERBOUND, LOWERBOUND)
        return pd.DataFrame(X_copy)



if __name__ == "__main__": 
    df, df_soc_eco = Load().Download()
    df.head()
    columns = [stg.BALANCE]
    df_treat = BalanceTransformer('num').fit_transform(df[columns])
    df_treat.head()
    df_treat.describe()



