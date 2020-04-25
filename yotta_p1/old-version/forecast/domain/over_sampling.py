#!/usr/bin/env python
# coding: utf-8
"""Module to perform oversampling on imbalanced classes.

Classes
-------
OverSampler

"""

from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN


class OverSampler():
    """
    Performs oversampling on imbalanced classes.

    Methods
    -------
    __init__
    fit_resample

    """

    def __init__(self, method="random", inactive=False):
        """Initilization of OverSampler instances.

        Parameters
        ----------
        method: str, default "random"
            Select on oversampling method
        inactive bool, default False
            Bypass oversampling
        """

        self.inactive = inactive

        if method == "random":
            self.sampler = RandomOverSampler()
        elif method == "smote":
            self.sampler = SMOTE()
        elif method == "adasyn":
            self.sampler = ADASYN()
        else:
            raise TypeError(f"The choice '{method}' for the argument 'method' is not available.")

    def fit_resample(self, X, y):
        """Performs oversampling.

        Parameters
        ----------
        X: pandas.DataFrame
            Features
        y: pandas.DataFrame
            Targets

        Returns
        -------
        X, y: pandas.DataFrame, pandas.DataFrame
            Oversampled features and targets
        """

        if self.inactive:
            return X, y
        else:
            return self.sampler.fit_resample(X, y)
