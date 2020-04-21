#!/usr/bin/env python
# coding: utf-8
"""Module to preprocess raw data.

Classes
-------
Preprocessing

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize

import forecast.settings as stg

class BayesianOpt:
    """
    Conduct Bayesian Optimisation process on models.

    Attributes
    ----------
    model: sklearn model

    Methods
    -------
    __init__

    """

    def __init__(self, clf, X, y):
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
        self.clf = clf
        self.X = X
        self.y = y
        self.n_features = X.shape[1]
        self.space = self.space_bound()
        self.res_gp = gp_minimize(self.objective, self.space, n_calls=200, random_state=0)
        print("Best score=%.4f" % self.res_gp.fun)

    def space_bound(self):
        space = [Integer(1, 5, name='max_depth'),
          Real(10**-5, 10**0, "log-uniform", name='learning_rate'),
          Integer(1, self.n_features, name='max_features'),
          Integer(2, 100, name='min_samples_split'),
          Integer(1, 100, name='min_samples_leaf')]
        return space

    @use_named_args(self.space)
    def objective(self, **params):
        self.clf.set_params(**params)

        return -np.mean(cross_val_score(self.clf, self.X, self.y, cv=5, n_jobs=-1,
                                        scoring="neg_mean_absolute_error"))

