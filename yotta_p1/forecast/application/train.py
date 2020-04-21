#!/usr/bin/env python
# coding: utf-8

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

import forecast.settings as stg
from forecast.domain import model_train, model_evaluation
from forecast.infrastructure.preprocessing import Preprocessing


def main(data_input, socio_eco_input, merge_file, model_path):
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

    # Preprocessing of raw data
    preprocessing = Preprocessing(data_input, socio_eco_input, merge_file)

    # Get features and target
    X, y = preprocessing.get_features_target()

    # Train test splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    # Training model
    model = model_train.train(X_train, y_train)

    # Evalutate model
    default_prediction_rate = 1 - y.sum() / len(y)
    model_evaluation.evaluation(model, X_test, y_test, default_prediction_rate)

    # Export the classifier to a file
    joblib.dump(model, model_path)


if __name__ == "__main__":
    data_input = os.path.join(stg.RAW_DATA_DIR, "data.csv")
    socio_eco_input = os.path.join(stg.RAW_DATA_DIR, "socio_eco.csv")
    merge_file = os.path.join(stg.INTERIM_DATA_DIR, "data_socio_merged.csv")
    model_path = os.path.join(stg.MODELS_DIR, "model.joblib")
    main(data_input, socio_eco_input, merge_file, model_path)