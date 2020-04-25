#!/usr/bin/env python
# coding: utf-8

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

    Returns
    -------
    clf : sklearn model trained
    """

    # Get transformer pipeline
    preprocessor = TransformerPipeline()
    # preprocessor = BaseTransformerPipeline(X_train)

    # Transform features
    X_transformed = preprocessor.fit_transform(X_train)

    # Oversampling
    X_resampled, y_resampled = OverSampler(method="random", inactive=False).fit_resample(X_transformed, y_train)

    # Model
    model = GradientBoostingClassifier()

    # Optimisation
    if optimisation:
        optimiser = BayesianOptimisation(model, X_resampled, y_resampled)
        optimiser.minimize()
        optimiser.display_result()

    # Fit the model
    model.fit(X_resampled, y_resampled)

    # Classifier
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)])

    return clf

