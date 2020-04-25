#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

import forecast.settings as stg
from forecast.domain.socio_eco_transformer import SocioEcoTransformer
from forecast.domain.date_transformer import DateTransformer
from forecast.domain.age_transformer import AgeTransformer
from forecast.domain.job_transformer import JobTransformer
from forecast.domain.status_transformer import StatusTransformer
from forecast.domain.education_transformer import EducationTransformer
from forecast.domain.bank_status_transformer import BankStatusTransformer
from forecast.domain.nb_day_last_contact_transformer import NbDayLastContactTransformer
from forecast.domain.nb_contact_transformer import NbContactTransformer
from forecast.domain.result_last_campaign_transformer import ResultLastCampaignTransformer
from forecast.domain.balance_transformer import BalanceTransformer


def FinalTransformerPipeline():
    """
    The transformer pipeline return the column transformer to do preprocessing
    """

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
   
    socio_eco_transformer = Pipeline(steps=[
        ('trans', SocioEcoTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    date_transformer = Pipeline(steps=[
        ('trans', DateTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    nb_contact_transformer = Pipeline(steps=[
        ('trans', NbContactTransformer(2, 2, 2)),
        ('imputer', SimpleImputer(missing_values= np.NaN, strategy='median')),
        ('scaler', StandardScaler())
    ])

    result_last_campaign_transformer = Pipeline(steps=[
        ('trans', ResultLastCampaignTransformer())
    ])

    balance_num_transformer = Pipeline(steps=[
        ('trans', BalanceTransformer("num")),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    status_transformer = Pipeline(steps=[
        ('trans', StatusTransformer()),
        ('imputer', SimpleImputer(strategy='median'))
    ])

    education_transformer = Pipeline(steps=[
        ('trans', EducationTransformer()),
        ('imputer', SimpleImputer(strategy='median'))
    ])   

    nb_day_last_contact_transformer = Pipeline(steps=[
        ('trans', NbDayLastContactTransformer()),
        ('imputer', StandardScaler())
    ])

    # # Numerical, categorical, socio eco features
    numeric_features = [stg.AGE]
    socio_eco_features = [stg.DATE_DATA, *stg.SOCIO_ECO_COLS]
    date_features = [stg.DATE_DATA]
    status_features = [stg.STATUS]
    education_features = [stg.EDUCATION]
    nb_contact_features = [stg.NB_CONTACT, stg.NB_CONTACT_LAST_CAMPAIGN]
    result_last_campaign_features = [stg.NB_DAY_LAST_CONTACT, stg.RESULT_LAST_CAMPAIGN]
    nb_day_last_contact_features = [stg.DATE_DATA, stg.NB_DAY_LAST_CONTACT]
    balance_features = [stg.BALANCE]

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('eco', socio_eco_transformer, socio_eco_features),
            ('date', date_transformer, date_features),
            ('num', numeric_transformer, numeric_features),
            ('contact', nb_contact_transformer, nb_contact_features),
            ('result', result_last_campaign_transformer, result_last_campaign_features),
            ('education', education_transformer, education_features),
            ('last', nb_day_last_contact_transformer, nb_day_last_contact_features),
            ('balnum', balance_num_transformer, balance_features),
            ('status', status_transformer, status_features)
    ])

    return preprocessor


def BaseTransformerPipeline(X_train):

    # Numerical transformer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Numrical and categorical features
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X_train.select_dtypes(include=['object']).columns
    
    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    return preprocessor


