#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns
# import pandas as pd
# from tabulate import tabulate

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import average_precision_score


def evaluation(model, X_test, y_test, default_prediction_rate):
    """Launch steps to asset the trained model and display tests models

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

    Returns
    -------
    No returns
    Display model metrics
    """
    print("model score: %.3f" % model.score(X_test, y_test))

    # Confusion matrix
    y_pred = model.predict(X_test)
    # Confusion matrix and other metrics
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    tn, fp, fn, tp = cm.ravel()
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    print("Précision: {}".format((tn+tp)/(tn+tp+fp+fn)))
    print("Sensibilté: {}".format(recall))
    print("Spécificité: {}".format(tn/(tn+fp)))
    print("TPR: {}".format(precision))
    print("F-score: {}".format(2*(precision*recall)/(precision+recall)))

    # Importance features
    # try:
    #     headers = ["name", "score"]
    #     values = sorted(zip(pd.DataFrame(X_test), model.steps[1][1].feature_importances_), key=lambda x: x[1] * -1)
    #     print(tabulate(values, headers, tablefmt="plain"))
    # except AttributeError:
    #     pass

    print(f"Taux de prediction pour un refus global : {default_prediction_rate:.3f}\n"
        f"Taux predit : {model.score(X_test, y_test):.3f}")

    plt.figure()
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='g')

    # calculate precision-recall curve
    y_probs = model.predict_proba(X_test)[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, y_probs)
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
