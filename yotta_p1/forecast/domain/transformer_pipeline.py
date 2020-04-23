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
from forecast.domain.NbDayLastContactTransformer import NbDayLastContactTransformer
from forecast.domain.NbContactTransformer import NbContactTransformer
from forecast.domain.ResultLastCampaignTransformer import ResultLastCampaignTransformer
from forecast.domain.balance_transformer import BalanceTransformer


def TransformerPipeline():

    # Numerical, categorical, socio eco features
    socio_eco_features = [stg.DATE_DATA, *stg.SOCIO_ECO_COLS]
    # numerical_features = []
    # categorical_features = []
    date_features = [stg.DATE_DATA]
    age_features = [stg.AGE]
    job_features = [stg.JOB_TYPE]
    status_features = [stg.STATUS]
    education_features = [stg.EDUCATION]
    bank_status_features = [*stg.BANK_STATUS_COL]
    nb_contact_features = [stg.NB_CONTACT, stg.NB_CONTACT_LAST_CAMPAIGN]
    result_last_campaign_features = [stg.NB_DAY_LAST_CONTACT, stg.RESULT_LAST_CAMPAIGN]
    nb_day_last_contact_features = [stg.DATE_DATA, stg.NB_DAY_LAST_CONTACT]
    balance_features = [stg.BALANCE]

    nb_day_last_contact_transformer = Pipeline(steps=[
        ('trans', NbDayLastContactTransformer()),
        ('imputer', StandardScaler())
    ])

    nb_contact_transformer = Pipeline(steps=[
        ('trans', NbContactTransformer()),
        ('imputer', SimpleImputer(missing_values= np.NaN, strategy='most_frequent')) 
    ])

    result_last_campaign_transformer = Pipeline(steps=[
        ('trans', ResultLastCampaignTransformer()),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    socio_eco_transformer = Pipeline(steps=[
        ('trans', SocioEcoTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ])

    date_transformer = Pipeline(steps=[
        ('trans', DateTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    age_transformer = Pipeline(steps=[
        ('trans', AgeTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    job_transformer = Pipeline(steps=[
        ('trans', JobTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    status_transformer = Pipeline(steps=[
        ('trans', StatusTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    education_transformer = Pipeline(steps=[
        ('trans', EducationTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    bank_status_transformer = Pipeline(steps=[
        ('trans', BankStatusTransformer()),
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    balance_cat_transformer = Pipeline(steps=[
        ('trans', BalanceTransformer("cat")),
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    balance_num_transformer = Pipeline(steps=[
        ('trans', BalanceTransformer("num")),
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
            ('eco', socio_eco_transformer, socio_eco_features),
            ('date', date_transformer, date_features),
            ('age', age_transformer, age_features),
            ('job', job_transformer, job_features),
            ('status', status_transformer, status_features),
            ('education', education_transformer, education_features),
            ('contact', nb_contact_transformer, nb_contact_features),
            ('last', nb_day_last_contact_transformer, nb_day_last_contact_features),
            ('result', result_last_campaign_transformer, result_last_campaign_features),
            ('bank', bank_status_transformer, bank_status_features),
            ('balcat', balance_cat_transformer, balance_features),
            ('balnum', balance_num_transformer, balance_features),
            # ('num', numerical_transformer, numerical_features),
            # ('cat', categorical_transformer, categorical_features),
            ])

    return preprocessor

def BaseTransformerPipeline(X_train):
    
    # Numerical transformer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Numrical and categorical features
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X_train.select_dtypes(include=['object']).columns

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    return preprocessor
