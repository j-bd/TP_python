#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

from forecast.domain import model_train, model_evaluation
import forecast.settings as stg


def main(input_file_name):
    """Launch main steps of model training

    Parameters
        ----------
    input_file_name: str
        String containing path to merge 'csv' dataset

    Returns
    -------
    No returns
    Save model
    """
    df_merged = pd.read_csv(input_file_name)
#    df_data = Treatment(df_data).run_preprocessing()

    # Features and target
    X = df_merged.drop([stg.SUBSCRIPTION, stg.DURATION_CONTACT], axis=1)
    df_merged[stg.SUBSCRIPTION] = df_merged[stg.SUBSCRIPTION].astype("category")
    y = df_merged[stg.SUBSCRIPTION].cat.codes
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    model = model_train.train(X_train, y_train)

    default_prediction_rate = 1 - y.sum() / len(y)
    model_evaluation.evaluation(model, X_test, y_test, default_prediction_rate)

    # Export the classifier to a file
    joblib.dump(model, "models/model.joblib")


if __name__ == "__main__":
    #random.seed(516)
    #input_file = "data/raw/data.csv"
    input_file = "data/interim/data_socio_merged.csv"
    main(input_file)
