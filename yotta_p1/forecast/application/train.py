#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import average_precision_score
import joblib

import forecast.settings as stg
from forecast.domain.socio_eco_transformer import SocioEcoTransformer
from forecast.domain.date_transformer import DateTransformer
from forecast.domain.age_transformer import AgeTransformer
from forecast.domain.job_transformer import JobTransformer
from forecast.domain.status_transformer import StatusTransformer
from forecast.domain.education_transformer import EducationTransformer



def main(input_file_name):
    """Launch main steps of model training

    Parameters
        ----------
    input_file_name: str
        String containing path to merge 'csv' dataset

    Returns
    -------
    No returns
    """
    df_merged = pd.read_csv(input_file_name)

    # Features and target
    X = df_merged.drop(stg.DATA_SUBSCRIPTION, axis=1)
    df_merged[stg.DATA_SUBSCRIPTION] = df_merged[stg.DATA_SUBSCRIPTION].astype("category")
    y = df_merged[stg.DATA_SUBSCRIPTION].cat.codes
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    model = train(X_train, y_train)

    default_prediction_rate = 1 - y.sum() / len(y)
    model_evaluation(model, X_test, y_test, default_prediction_rate)

    # Export the classifier to a file
    joblib.dump(model, "models/model.joblib")


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
    date_features = [stg.DATA_DATE]
    age_features = [stg.DATA_AGE]
    job_features = [stg.DATA_JOB_TYPE]
    status_features = [stg.DATA_STATUS]
    education_features = [stg.DATA_EDUCATION]

    # Column transformer
    preprocessor = ColumnTransformer(
        transformers=[
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
            ('classifier', GradientBoostingClassifier())])
    gb.fit(X_train, y_train)

    return gb

def model_evaluation(model, X_test, y_test, default_prediction_rate):
    """Launch steps to asset the trained model and display tests models

    Parameters
        ----------
    model: sklearn model
        Trained model

    Returns
    -------
    No returns
    """
    print("model score: %.3f" % model.score(X_test, y_test))

    # Confusion matrix
    y_pred = model.predict(X_test)
    print(confusion_matrix(y_test, y_pred))



    print(f"Taux de prediction pour un refus global : {default_prediction_rate:.3f}\n"
        f"Taux predit : {model.score(X_test, y_test):.3f}")

    plt.figure()
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='g')

    # calculate precision-recall curve
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred)
    # calculate F1 score
    f1 = f1_score(y_test, y_pred)
    # calculate precision-recall AUC
    pr_auc = auc(recall, precision)
    # calculate average precision score
    ap = average_precision_score(y_test, y_pred)
    print('f1=%.3f auc=%.3f ap=%.3f' % (f1, pr_auc, ap))

    plt.figure()
    # plot no skill
    plt.plot([0, 1], [0.88, 0.88], linestyle='--', label="Seuil bas")
    # plot the precision-recall curve for the model
    plt.plot(recall, precision, marker='.', label="Courbe Precision Recall")
    plt.title("Courbe Precision Recall")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.legend()
    plt.show()


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
    main(input_file)
