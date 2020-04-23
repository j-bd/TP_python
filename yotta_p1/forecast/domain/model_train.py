#!/usr/bin/env python
# coding: utf-8

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV, StratifiedKFold, RandomizedSearchCV

from forecast.domain.transformer_pipeline import TransformerPipeline, BaseTransformerPipeline
from forecast.domain.over_sampling import OverSampler
from forecast.domain.bayesian_optimisation import BayesianOptimisation


def train(X_train, y_train, args):
    """Setup training pipeline and launch model training

    Parameters
        ----------
    X_train: pandas.DataFrame
        explanatory variables
    y_train: pandas.Series
        target variable

    Returns
    -------
    No returns
    """

    # Get transformer pipeline
    preprocessor = TransformerPipeline()
    # preprocessor = BaseTransformerPipeline(X_train)

    # Transform features
    X_transformed = preprocessor.fit_transform(X_train)

    # Oversampling
    X_resampled, y_resampled = OverSampler(method="random", inactive=False).fit_resample(X_transformed, y_train)

    # Model
    model = GradientBoostingClassifier() # XGBClassifier() #GradientBoostingClassifier()

    # Optimisation
    if args.optimisation:
        optimiser = BayesianOptimisation(model, X_resampled, y_resampled)
        optimiser.minimize()
        optimiser.display_result()

    #params = {
    #    'loss': ['deviance','exponential'],
    #    'learning_rate': [0.001, 0.01, 0.1],
    #    'n_estimators': [10, 20, 50],
    #    'criterion': ['friedman_mse', 'mse', 'mae'],
    #    'min_samples_split': [1, 2, 5],
    #    'min_samples_leaf' : [1, 2, 5],
    #    'max_depth' : [3, 5]
    #}
    #cross_val = StratifiedKFold(n_splits=5, shuffle=False, random_state=None)
    #cross_val.split(X_train.columns, y_train.columns)
    #modelCV = RandomizedSearchCV(model, params, n_iter = 3, cv= 5)

    # Fit the model
    model.fit(X_resampled, y_resampled)

    # Classifier
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)])

    return clf

