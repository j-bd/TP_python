#!/usr/bin/env python
# coding: utf-8

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier

from forecast.domain.transformer_pipeline import TransformerPipeline, BaseTransformerPipeline
from forecast.domain.over_sampling import OverSampler
from forecast.domain.bayesian_optimisation import BayesianOptimisation


def train(X_train, y_train, optimisation):
    """Setup training pipeline and launch model training

    Parameters
        ----------
    X_train: pandas.DataFrame
        explanatory variables
    y_train: pandas.Series
        target variable
    optimisation: boolean
        set True by operator when Bayesian Optimisation expected

    Returns
    -------
    clf : sklearn model trained
    """

    # Get transformer pipeline
    preprocessor = TransformerPipeline()
    # preprocessor = BaseTransformerPipeline(X_train)

    # Transform features
    logging.info('Data Preprocessing on going ...')
    X_transformed = preprocessor.fit_transform(X_train)

    # Oversampling
    logging.info('Data Oversampling on going ...')
    X_resampled, y_resampled = OverSampler(
        method="random", inactive=False).fit_resample(X_transformed, y_train)

    # Model
    model = GradientBoostingClassifier()

    # Optimisation
    if optimisation:
        logging.info('Bayesian Optimisation hyperparameters on going ...')
        optimiser = BayesianOptimisation(model, X_resampled, y_resampled)
        optimiser.minimize()
        optimiser.display_result()
        model.set_params(**optimiser.get_best_params)
        logging.info('Bayesian Optimisation hyperparameters done')

    # Fit the model
    logging.info('Model fitting on going ...')
    model.fit(X_resampled, y_resampled)

    # Classifier
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)])

    return clf
