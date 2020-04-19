#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.compose import ColumnTransformer

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import confusion_matrix

import joblib

from forecast.domain.socio_eco_transformer import SocioEcoTransformer
from forecast.domain.date_transformer import DateTransformer
from forecast.domain.age_transformer import AgeTransformer
from forecast.domain.job_transformer import JobTransformer
from forecast.domain.status_transformer import StatusTransformer

import forecast.settings as stg


def train(input_file_name):
    df_data = pd.read_csv(input_file_name)

    # Features and target
    X = df_data.drop('SUBSCRIPTION', axis=1)
    y = df_data['SUBSCRIPTION']

    # Training and testing set separation
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # It’s important to stratify y when doing a train_test_split on imbalanced classes, or on a small dataset.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

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
        ('jobtrans', StatusTransformer()),
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
    numeric_features = df_data.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = df_data.select_dtypes(include=['object']).drop(['SUBSCRIPTION'], axis=1).columns
    numeric_features = [x for x in numeric_features if x not in stg.SOCIO_ECO_COLS]
    socio_eco_features = stg.SOCIO_ECO_COLS + [stg.DATE_SOCIO_COL]
    date_features = [stg.DATA_DATE]
    age_features = [stg.DATA_AGE]
    job_features = [stg.DATA_JOB_TYPE]
    status_features = [stg.DATA_STATUS]

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('eco', socio_eco_transformer, socio_eco_features),
            ('date', date_transformer, date_features),
            ('age', age_transformer, age_features),
            ('job', job_transformer, job_features),
            ('status', status_transformer, status_features),
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    # Classifier
    gb = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', GradientBoostingClassifier())])
    gb.fit(X_train, y_train)
    print("model score: %.3f" % gb.score(X_test, y_test))

    # Confusion matrix
    y_pred = gb.predict(X_test)
    print(confusion_matrix(y_test, y_pred))

    # Export the classifier to a file
    joblib.dump(gb, "models/model.joblib")

    # # Model selection
    # classifiers = [
    #     KNeighborsClassifier(3), #0.886
    #     SVC(kernel="rbf", C=0.025, probability=True), # 0.885
    #     DecisionTreeClassifier(), #0.882
    #     RandomForestClassifier(), # 0.900
    #     AdaBoostClassifier(), #0.901
    #     GradientBoostingClassifier() #0.903
    #     ]
    # for classifier in classifiers:
    #     pipe = Pipeline(
    #         steps=[
    #             ('preprocessor', preprocessor),
    #             ('classifier', classifier)])
    #     pipe.fit(X_train, y_train)
    #     print(classifier)
    #     print("model score: %.3f" % pipe.score(X_test, y_test))

    # # Grid search (Random Forest)
    # rf = Pipeline(
    #     steps=[
    #         ('preprocessor', preprocessor),
    #         ('classifier', RandomForestClassifier())])
    # param_grid = {
    #     'classifier__n_estimators': [1, 2, 3, 4, 5],
    #     'classifier__max_features': ['auto', 'sqrt', 'log2'],
    #     'classifier__max_depth' : [4, 5, 6, 7, 8],
    #     'classifier__criterion' :['gini', 'entropy']}
    # #CV = GridSearchCV(rf, param_grid, n_jobs= 1)
    # CV = GridSearchCV(rf, param_grid, verbose = 1, n_jobs = 6) # n_jobs = -1)
    # CV.fit(X_train, y_train)
    # print(CV.best_params_)
    # # {'classifier__criterion': 'entropy', 'classifier__max_depth': 4, 'classifier__max_features': 'auto', 'classifier__n_estimators': 1}
    # print(CV.best_score_)
    # # 0.889692192504009
    # print("model score: %.3f" % CV.score(X_test, y_test))
    # # model score: 0.893

    # # Grid search (knn)
    # knn = Pipeline(
    #     steps=[
    #         ('preprocessor', preprocessor),
    #         ('classifier', KNeighborsClassifier())])
    # param_grid = {
    #     'classifier__n_neighbors': [3, 5, 11, 19],
    #     'classifier__weights': ['uniform', 'distance'],
    #     'classifier__metric': ['euclidean', 'manhattan']}
    # gs = GridSearchCV(
    #     knn,
    #     param_grid,
    #     verbose = 1,
    #     cv = 3,
    #     n_jobs = 6) # n_jobs = -1)
    # gs_results = gs.fit(X_train, y_train)
    # print(gs_results.best_params_)
    # # {'classifier__metric': 'euclidean', 'classifier__n_neighbors': 19, 'classifier__weights': 'distance'}
    # print(gs_results.best_score_)
    # # 0.898277390052066
    # print("model score: %.3f" % gs.score(X_test, y_test))
    # # model score: 0.900

if __name__ == "__main__":
    #input_file = "data/raw/data.csv"
    input_file = "data/interim/data_socio_merged.csv"
    train(input_file)
