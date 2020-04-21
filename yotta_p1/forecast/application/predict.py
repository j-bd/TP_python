#!/usr/bin/env python
# coding: utf-8

import os
import joblib
from sklearn.model_selection import train_test_split

import forecast.settings as stg
from forecast.infrastructure.preprocessing import Preprocessing


def main(data_input, socio_eco_input, merge_file, model_path):

    # Preprocessing of raw data
    preprocessing = Preprocessing(data_input, socio_eco_input, merge_file)

    # Features and target
    X, y = preprocessing.get_features_target()

    # It’s important to stratify y when doing a train_test_split on imbalanced classes, or on a small dataset.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    # Load the model from disk
    loaded_model = joblib.load(model_path)

    # Score of the model
    print("model score: %.3f" % loaded_model.score(X_test, y_test))


if __name__ == "__main__":
    data_input = os.path.join(stg.RAW_DATA_DIR, "data.csv")
    socio_eco_input = os.path.join(stg.RAW_DATA_DIR, "socio_eco.csv")
    merge_file = os.path.join(stg.INTERIM_DATA_DIR, "data_socio_merged.csv")
    model_path = os.path.join(stg.MODELS_DIR, "model.joblib")
    main(data_input, socio_eco_input, merge_file, model_path)
