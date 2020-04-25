#!/usr/bin/env python
# coding: utf-8
"""Module to optimise model.

Class
-------
Bayesian Optimisation

METHODS
---------
space_definition
space_gradient_boosting
space_svm
space_random_forest
space_adaboost
wrapper
minimize
display_result
get_best_params

"""

import numpy as np
from sklearn.model_selection import cross_val_score
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize
from skopt.plots import plot_convergence, plot_evaluations, plot_objective



class BayesianOptimisation:
    """Seek the best parameters with Bayesian Method

    Parameters
    ----------
    model: sklearn model
    X: numpy ndarray
    y: pandas.Series

    RETURNS
    -------
    best_params: dict
        if get_best_params method is called
    """

    def __init__(self, model, X, y):
        self.model = model
        self.X = X
        self.y = y
        self.n_features = self.X.shape[1]
        self.space = self.space_definition()

    def space_definition(self):
        model_name = str(type(self.model)).split("'")[1].split(".")[-1]
        if model_name == 'GradientBoostingClassifier':
            space = self.space_gradient_boosting()
        elif model_name == 'SVC':
            space = self.space_svm()
        elif model_name == 'RandomForestClassifier':
            space = self.space_random_forest()
        elif model_name == 'AdaBoostClassifier':
            space = self.space_adaboost()
        else:
            print(f"""
                  Prameters for {type(self.model)}
                  is not implemented. Optimisation can not be done.
                  Please, create a new function named 'def space_{model_name}()'
                  and call it with 'elif model_name == '{model_name}':
                  """)
            return None
        return space

    def space_gradient_boosting(self):
        """Define bounds for the gradient boosting model parameters"""
        space = [
            Integer(1, 2, name='max_depth'),
            Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
            Integer(1, self.n_features, name='max_features'),
            Integer(2, 20, name='min_samples_split'),
            Integer(1, 10, name='min_samples_leaf')
        ]
        return space

    def space_svm(self):
        """Define bounds for the svm model parameters"""
        space = [
            Real(1e-6, 1e+6, "log-uniform", name='C'),
            Categorical(['linear', 'poly', 'rbf', 'sigmoid'], name='kernel'),
            Real(1e-6, 1e+1, "log-uniform", name='gamma')
        ]
        return space

    def space_random_forest(self):
        """Define bounds for the random forest model parameters"""
        space = [
            Integer(1, 2, name='max_depth'),
            Categorical(['gini', 'entropy'], name='criterion'),
            Integer(1, self.n_features, name='max_features'),
            Integer(2, 20, name='min_samples_split'),
            Integer(1, 10, name='min_samples_leaf')
        ]
        return space

    def space_adaboost(self):
        """Define bounds for the adaboost model parameters"""
        space = [
            Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
            Categorical(['SAMME', 'SAMME.R'], name='algorithm')
        ]
        return space

    def wrapper(self):
        @use_named_args(self.space)
        def objective(**params):
            self.model.set_params(**params)
            return -np.mean(
                cross_val_score(self.model, self.X, self.y, cv=10, n_jobs=-1,
                                scoring="neg_mean_absolute_error")
            )
        return objective

    def minimize(self):
        self.res_gp = gp_minimize(
            func=self.wrapper(), dimensions=self.space, n_calls=15, random_state=0
        )

    def display_result(self):
        print("Best score=%.4f" % self.res_gp.fun)
        print(f"""Best parameters:
            - max_depth={self.res_gp.x[0]:d}
            - learning_rate={self.res_gp.x[1]:.6f}
            - max_features={self.res_gp.x[2]:d}
            - min_samples_split={self.res_gp.x[3]:d}
            - min_samples_leaf={self.res_gp.x[4]:d}""")
        plot_convergence(self.res_gp)
        _ = plot_evaluations(self.res_gp, bins=10)
        _ = plot_objective(self.res_gp)

    @property
    def get_best_params(self):
        best_params = {'max_depth':self.res_gp.x[0], 'learning_rate':self.res_gp.x[1],
                       'max_features':self.res_gp.x[2], 'min_samples_split':self.res_gp.x[3],
                       'min_samples_leaf':self.res_gp.x[4]}
        return best_params
