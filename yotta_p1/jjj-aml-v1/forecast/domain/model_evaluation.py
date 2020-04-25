#!/usr/bin/env python
# coding: utf-8
"""Module to evaluate models.

FUNCTIONS
---------

get_transformer_feature_names
evaluation

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import average_precision_score
from sklearn.metrics import classification_report


def get_transformer_feature_names(column_transformer):
    """Get ordered list of features names corresponding
    to transformed dataframe

    PARAMETERS
    ----------
    column_transformer: sklearn.compose.ColumnTransformer

    RETURNS
    -------
    output_features: list

    """

    output_features = []

    for name, pipe, features in column_transformer.transformers_:
        if name == 'remainder':
            continue

        step_names = [step[0] for step in pipe.steps]
        if 'trans' in step_names:
            trans_features = pipe.named_steps['trans'].get_feature_names()
        else:
            trans_features = features
        if 'onehot' in step_names:
            trans_features = pipe.named_steps['onehot'].get_feature_names(trans_features)

        output_features.extend(trans_features)

    return output_features


def evaluation_dev(model, X_test, y_test, default_prediction_rate, threshold=.5):
    """Launch steps to asset the trained model and display tests models.

    Parameters
    ----------
    model: sklearn model
        Trained model
    X_test: pandas.DataFrame
        explanatory variables
    y_test: pandas.Series
        target variable
    default_prediction_rate: float
        percent value of no in full dataset
    threshold: int
        threshold for the prediction

    Returns
    -------
    No returns
    Display model metrics
    """
    print("model score: %.3f" % model.score(X_test, y_test))

    # Confusion matrix
    y_pred = model.predict(X_test)
    # Confusion matrix and other metrics

    # Change threshold
    y_scores = model.predict_proba(X_test)[:, 1]
    y_pred_adj = [1 if y >= threshold else 0 for y in y_scores]
    print()
    print(classification_report(y_test, y_pred_adj))

    # Importance features
    feature_names = get_transformer_feature_names(model.steps[0][1])
    #print("len features name:", len(feature_names))
    #print("len features impo:", len(model.steps[1][1].feature_importances_))
    try:
        headers = ["name", "score"]
        values = sorted(zip(feature_names, model.steps[1][1].feature_importances_), key=lambda x: x[1] * -1)
        #values = zip(feature_names, model.steps[1][1].feature_importances_)
        print(tabulate(values, headers, tablefmt="plain"))
    except AttributeError:
        pass

    print(f"Taux de prediction pour un refus global : {default_prediction_rate:.3f}\n"
        f"Taux predit : {model.score(X_test, y_test):.3f}")

    # plt.figure()
    # cm = confusion_matrix(y_test, y_pred)
    # sns.heatmap(cm, annot=True, fmt='g')

    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    print()
    print(classification_report(y_test, y_pred)) #, target_names=[0, 1]))

    tn, fp, fn, tp = cm.ravel()
    precision = tp/(tp+fp)*100
    recall = tp/(tp+fn)*100

    print("Précision: {}".format((tn+tp)/(tn+tp+fp+fn)*100))
    print("Sensibilté: {}".format(recall))
    print("Spécificité: {}".format(tn/(tn+fp)*100))
    print("TPR: {}".format(precision))
    print("F-score: {}".format(2*(precision*recall)/(precision+recall)))

    # calculate precision-recall curve
    y_probs = model.predict_proba(X_test)[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, y_probs)

    # calculate F1 score
    f1 = f1_score(y_test, y_pred)

    # calculate precision-recall AUC
    pr_auc = auc(recall, precision)

    # calculate average precision score
    ap = average_precision_score(y_test, y_pred)
    print('f1=%.3f auc=%.3f ap=%.3f ' % (f1, pr_auc, ap))
 
    # plt.figure()
    # # plot no skill
    # plt.plot([0, 1], [0.88, 0.88], linestyle='--', label="Seuil bas")
    # # plot the precision-recall curve for the model
    # plt.plot(recall, precision, marker='.', label="Courbe Precision Recall")
    # plt.title("Courbe Precision Recall")
    # plt.xlabel("Recall")
    # plt.ylabel("Precision")
    # plt.legend()
    # plt.show()


def evaluation(model, X_test, y_test, threshold=.5):
    """Launch steps to asset the trained model and display tests models.

    Parameters
    ----------
    model: sklearn model
        Trained model
    X_test: pandas.DataFrame
        explanatory variables
    y_test: pandas.Series
        target variable
    threshold: int
        threshold for the prediction
    """
    y_scores = model.predict_proba(X_test)[:, 1]
    y_pred_adj = [1 if y >= threshold else 0 for y in y_scores]
    print()
    print(classification_report(y_test, y_pred_adj))
