#!/usr/bin/env python
# coding: utf-8
"""Module to optimise model.

Function
-------
Bayesian Optimisation

"""

import numpy as np
from sklearn.model_selection import cross_val_score
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize
from skopt.plots import plot_convergence, plot_evaluations, plot_objective



def objective_wrapper(model, X, y):
    """Seek the best parameters with Bayesian Method

    Parameters
    ----------
    model: sklearn model
    X: numpy ndarray
    y: pandas.Series
    """
    def space_gradient_boosting():
        """Define bounds for the gradient boosting model parameters"""
        space = [
            Integer(1, 2, name='max_depth'),
            Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
            Integer(1, n_features, name='max_features'),
            Integer(2, 20, name='min_samples_split'),
            Integer(1, 10, name='min_samples_leaf')
        ]
        return space

    def space_svm():
        """Define bounds for the svm model parameters"""
        space = [
            Real(1e-6, 1e+6, "log-uniform", name='C'),
            Categorical(['linear', 'poly', 'rbf', 'sigmoid'], name='kernel'),
            Real(1e-6, 1e+1, "log-uniform", name='gamma')
        ]
        return space

    def space_random_forest():
        """Define bounds for the random forest model parameters"""
        space = [
            Integer(1, 2, name='max_depth'),
            Categorical(['gini', 'entropy'], name='criterion'),
            Integer(1, n_features, name='max_features'),
            Integer(2, 20, name='min_samples_split'),
            Integer(1, 10, name='min_samples_leaf')
        ]
        return space

    def space_adaboost():
        """Define bounds for the adaboost model parameters"""
        space = [
            Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
            Categorical(['SAMME', 'SAMME.R'], name='algorithm')
        ]
        return space

    n_features = X.shape[1]
    model_name = str(type(model)).split("'")[1].split(".")[-1]
    print(model_name, "////", model.__module__)

    if model_name == 'GradientBoostingClassifier':
        space = space_gradient_boosting()
    elif model_name == 'SVC':
        space = space_svm()
    elif model_name == 'RandomForestClassifier':
        space = space_random_forest()
    elif model_name == 'AdaBoostClassifier':
        space = space_adaboost()
    else:
        print(f"""
              Prameters for {type(model)}
              is not implemented. Optimisation can not be done.
              Please, create a new function named 'def space_{model_name}()' and
              call it with 'elif model_name == '{model_name}':
              """)
        return None

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
            - min_samples_leaf={res_gp.x[4]:d}""")
        plot_convergence(res_gp)
        _ = plot_evaluations(res_gp, bins=10)
        _ = plot_objective(res_gp)


    res_gp = gp_minimize(
        func=objective, dimensions=space, n_calls=200, random_state=0
    )
    display_result(res_gp)
