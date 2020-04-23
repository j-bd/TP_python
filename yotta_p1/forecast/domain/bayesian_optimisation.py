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
from skopt.plots import plot_convergence, plot_evaluations, plot_objective

import forecast.settings as stg

#
#sklearn.ensemble._gb /// _gb
#sklearn.svm._classes /// _classes
#sklearn.ensemble._forest /// _forest
#sklearn.ensemble._weight_boosting /// _weight_boosting
#l_mod = [GradientBoostingClassifier(), SVC(), RandomForestClassifier(), AdaBoostClassifier()]



def objective_wrapper(model, X, y, verbose=1):
    """Seek the best parameters with Bayesian Method

    Parameters
    ----------
    model: sklearn model
    X: numpy ndarray
    y: pandas.Series
    """
    def space_gradient_boosting():
        space = [
            Integer(1, 2, name='max_depth'),
            Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
            Integer(1, n_features, name='max_features'),
            Integer(2, 20, name='min_samples_split'),
            Integer(1, 10, name='min_samples_leaf')
        ]
        return space

    def space_svm():
        space = [
            Integer(1, 2, name='max_depth'),
            Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
            Integer(1, n_features, name='max_features'),
            Integer(2, 20, name='min_samples_split'),
            Integer(1, 10, name='min_samples_leaf')
        ]
        return space

    def space_random_forest():
        return space

    def space_adaboost():
        return space

    n_features = X.shape[1]/10
    model_name = model.__module__.split('.')[-1]

    if model_name == '_gb':
        space = space_gradient_boosting()
    elif model_name == '_classes':
        space = space_svm()
    elif model_name == '_forest':
        space = space_random_forest()
    elif model_name == '_weight_boosting':
        space = space_adaboost()
    else:
        print(f"""
              Prameters for {model.__module__} is not implemented. Please,
              create a new function named 'space_model_name' and call it with
              'elif model_name == {model.__module__.split('.')[-1]}'
              """)

    @use_named_args(space)
    def objective(**params):
        model.set_params(**params)
        return -np.mean(
            cross_val_score(model, X, y, cv=5, n_jobs=-1,
                            scoring="neg_mean_absolute_error")
        )

    def display_result(res_gp):
        print("Best score=%.4f" % res_gp.fun)
        print(f"""Best parameters:
            - max_depth={res_gp.x[0]:d}
            - learning_rate={res_gp.x[1]:.6f}
            - max_features={res_gp.x[2]:d}
            - min_samples_split={res_gp.x[3]:d}
            - min_samples_leaf={res_gp.x[4]:d}"""
        )
        plot_convergence(res_gp)
        _ = plot_evaluations(res_gp, bins=10)
        _ = plot_objective(res_gp)


    res_gp = gp_minimize(
        func=objective, dimensions=space, n_calls=200, random_state=0
    )
    display_result(res_gp)










#def optimi(model, X, y):
#    n_features = X.shape[1]
#
#    space = [
#        Integer(1, 5, name='max_depth'),
#        Real(10**-5, 10**0, "log-uniform", name='learning_rate'),
#        Integer(1, n_features, name='max_features'),
#        Integer(2, 100, name='min_samples_split'),
#        Integer(1, 100, name='min_samples_leaf')
#    ]

#def objective_wrapper(model, X, y):
#    print("bagin objective_wrapper")
#    n_features = X.shape[1]
#
#    space = [
#        Integer(1, 5, name='max_depth'),
#        Real(10**-5, 10**0, "log-uniform", name='learning_rate'),
#        Integer(1, n_features, name='max_features'),
#        Integer(2, 100, name='min_samples_split'),
#        Integer(1, 100, name='min_samples_leaf')
#    ]
#
#    @use_named_args(space)
#    def objective(self, **params):
#        print("in objective")
#        self.model.set_params(**params)
#
#        return -np.mean(cross_val_score(self.model, self.X, self.y, cv=5, n_jobs=-1,
#                                        scoring="neg_mean_absolute_error"))
#
#
#
#
#    res_gp = gp_minimize(
#        func=objective(), dimensions=space, n_calls=200, random_state=0
#    )
#    print("Best score=%.4f" % res_gp.fun)
























#space = [Integer(1, 5, name='max_depth'),
#  Real(10**-5, 10**0, "log-uniform", name='learning_rate'),
#  Integer(1, n_features, name='max_features'),
#  Integer(2, 100, name='min_samples_split'),
#  Integer(1, 100, name='min_samples_leaf')]

#
#class BayesianOpt:
#    """
#    Conduct Bayesian Optimisation process on models.
#
#    Attributes
#    ----------
#    model: sklearn model
#
#    Methods
#    -------
#    __init__
#
#    """
#
#    def __init__(self, clf, X, y):
#        """ Initialize class.
#
#        Create data and socio eco dataframes from corresponding input files and merge them.
#
#        Parameters
#        ----------
#        path_to_input_data: string
#        path_to_input_socio_eco: string
#        path_to_output: string
#        save_output: bool, default True
#        target_name: str, default stg.SUBSCRIPTION
#        """
#        self.clf = clf
#        self.X = X
#        self.y = y
#        self.n_features = X.shape[1]
#        self.space = self.space_bound()
#        self.res_gp = gp_minimize(self.objective, self.space, n_calls=200, random_state=0)
#        print("Best score=%.4f" % self.res_gp.fun)
#
#
#    def space_bound(self):
#        space = [Integer(1, 5, name='max_depth'),
#          Real(10**-5, 10**0, "log-uniform", name='learning_rate'),
#          Integer(1, self.n_features, name='max_features'),
#          Integer(2, 100, name='min_samples_split'),
#          Integer(1, 100, name='min_samples_leaf')]
#        return space
#
#    @use_named_args(space)
#    def objective(self, **params):
#        self.clf.set_params(**params)
#
#        return -np.mean(cross_val_score(self.clf, self.X, self.y, cv=5, n_jobs=-1,
#                                        scoring="neg_mean_absolute_error"))









