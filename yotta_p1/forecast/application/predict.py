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

import joblib

def predict():
    df_data = pd.read_csv("data/raw/data.csv")
    # print(df_data.head())
    # print(df_data.dtypes)

    # Features and target
    X = df_data.drop('SUBSCRIPTION', axis=1)
    y = df_data['SUBSCRIPTION']

    # Training and testing set separation
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # It’s important to stratify y when doing a train_test_split on imbalanced classes, or on a small dataset.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    # Load the model from disk
    loaded_model = joblib.load("models/model.joblib")

    # Score of the model
    print("model score: %.3f" % loaded_model.score(X_test, y_test))


if __name__ == "__main__":
    predict()
