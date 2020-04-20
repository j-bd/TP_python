#!/usr/bin/env python
# coding: utf-8


from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
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
from forecast.domain.Treatment import Treatment
from forecast.domain.QuantitativeTransformer import QuantitativeTransformer


# New packages added
#import random
#from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
#from imblearn.over_sampling import SMOTE


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
    #print('Shape before SMOTE')
    #print(X_train.shape[0])

    # Use SMOTE for the oversampling, create new rows for SUBSCRIPTION = 'Yes'
    # /!\ Need LabelEncoding to work /!\
    #oversample = SMOTE()
    #X_train, y_train = oversample.fit_resample(X_train, y_train)

    # Make sur it's usefull:
    #print('Shape before SMOTE')
    #print(X_train.shape[0])


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

    # Numerical transformer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Numrical, categorical, socio eco features
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X_train.select_dtypes(include=['object']).columns
    numeric_features = [x for x in numeric_features if x not in stg.SOCIO_ECO_COLS]
    socio_eco_features = stg.SOCIO_ECO_COLS + [stg.DATE_SOCIO_COL]
    date_features = [stg.DATE_DATA]
    age_features = [stg.AGE]
    job_features = [stg.JOB_TYPE]
    status_features = [stg.STATUS]
    education_features = [stg.EDUCATION]

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
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    # Classifier
    gb = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression())]) # XGBClassifier()
    gb.fit(X_train, y_train)

    return gb

