#!/usr/bin/env python
# coding: utf-8

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV

import forecast.settings as stg
from forecast.domain.socio_eco_transformer import SocioEcoTransformer
from forecast.domain.date_transformer import DateTransformer
from forecast.domain.age_transformer import AgeTransformer
from forecast.domain.job_transformer import JobTransformer
from forecast.domain.status_transformer import StatusTransformer
from forecast.domain.education_transformer import EducationTransformer
from forecast.domain.bank_status_transformer import BankStatusTransformer
from forecast.domain import bayesian_optimisation as bay_op
#from forecast.domain.Treatment import Treatment
#from forecast.domain.QuantitativeTransformer import QuantitativeTransformer
from forecast.domain.over_sampling import OverSampler


def train(X_train, y_train):
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

    # Numerical, categorical, socio eco features
    socio_eco_features = [stg.DATE_DATA, *stg.SOCIO_ECO_COLS]
    numerical_features = [stg.BALANCE, stg.NB_CONTACT, stg.NB_DAY_LAST_CONTACT, stg.NB_CONTACT_LAST_CAMPAIGN]
    categorical_features = [stg.CONTACT, stg.RESULT_LAST_CAMPAIGN]
    date_features = [stg.DATE_DATA]
    age_features = [stg.AGE]
    job_features = [stg.JOB_TYPE]
    status_features = [stg.STATUS]
    education_features = [stg.EDUCATION]
    bank_status_features = [*stg.BANK_STATUS_COL]


    # Modify RESULT_LAST_CAMPAIGN , drop DURATION_CONTACT, create AT_DEBIT and PRECARITY,CAT_CONTACT_LAST_CAMPAIGN,CAT_CONTACT
    #quanti_transformer = Pipeline(steps=[
    #   ('treat', QuantitativeTransformer()),
     #   ('scaler', StandardScaler())])

    # Socio eco transformer
    socio_eco_transformer = Pipeline(steps=[
        ('sociotrans', SocioEcoTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    date_transformer = Pipeline(steps=[
        ('datetrans', DateTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    age_transformer = Pipeline(steps=[
        ('agetrans', AgeTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    job_transformer = Pipeline(steps=[
        ('jobtrans', JobTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    status_transformer = Pipeline(steps=[
        ('statustrans', StatusTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    education_transformer = Pipeline(steps=[
        ('educationtrans', EducationTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    bank_status_transformer = Pipeline(steps=[
        ('bankstatustrans', BankStatusTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Numerical transformer
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            #('qti', quanti_transformer, quanti_features),
            ('eco', socio_eco_transformer, socio_eco_features),
            ('date', date_transformer, date_features),
            ('age', age_transformer, age_features),
            ('job', job_transformer, job_features),
            ('status', status_transformer, status_features),
            ('education', education_transformer, education_features),
            ('bank', bank_status_transformer, bank_status_features),
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)])

    # Transform features
    X_transformed = preprocessor.fit_transform(X_train)

    # Oversampling
    X_resampled, y_resampled = OverSampler(method="random", inactive=False).fit_resample(X_transformed, y_train)

    # Model
    model = GradientBoostingClassifier() # XGBClassifier() #GradientBoostingClassifier()

    # Optimisation
    print('before opt')
#    bay_op.objective_wrapper(model, X_resampled, y_resampled)

    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.model_selection import cross_val_score
    from skopt.space import Real, Integer
    from skopt.utils import use_named_args
    from skopt import gp_minimize

    n_features = X_resampled.shape[1]/10

    space = [
        Integer(1, 2, name='max_depth'),
        Real(10**-1, 10**0, "log-uniform", name='learning_rate'),
        Integer(1, n_features, name='max_features'),
        Integer(2, 20, name='min_samples_split'),
        Integer(1, 10, name='min_samples_leaf')
    ]

    @use_named_args(space)
    def objective(**params):
        print("in objective")
        model.set_params(**params)

        return -np.mean(cross_val_score(model, X_resampled, y_resampled, cv=5, n_jobs=-1,
                                        scoring="neg_mean_absolute_error"))

    res_gp = gp_minimize(
        func=lambda x: objective(x), dimensions=space, n_calls=200, random_state=0
    )
    print("Best score=%.4f" % res_gp.fun)

    print('after opt')

    # Fit the model
    model.fit(X_resampled, y_resampled)

    # Classifier
    clf = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('model', model)])

    return clf
