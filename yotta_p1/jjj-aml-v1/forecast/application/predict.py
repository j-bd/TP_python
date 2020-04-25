#!/usr/bin/env python
# coding: utf-8

"""Module to make predictions.

Example
-------
Script could be run with the following command line

    $ python forecast/application/predict.py

Input datasets localizations can be specified with

    $ python forecast/application/predict.py -d path/to/data_file -s path/to/socio_eco_file

Model localization can be specified with

    $ python forecast/application/predict.py -m path/to/model_file

Predict dataset localization can be specified with

    $ python forecast/application/predict.py -p path/to/predict_file

"""

import pandas as pd
import joblib

from forecast.infrastructure.command_line_parser import PredictCommandLineParser
from forecast.infrastructure.preprocessing import Preprocessing
import forecast.settings as stg


def main():
    """Make prediction on input datasets."""

    # Command line parser
    parser = PredictCommandLineParser()
    args = parser.parse_args()

    # Preprocessing of raw data
    preprocessing = Preprocessing(args.data_input, args.socio_eco_input)
    preprocessing.do_preprocessing()

    # Get features
    X = preprocessing.get_features()

    # Load the model from disk
    loaded_model = joblib.load(args.model_input)

    # Predict target
    X[stg.PREDICTION] = pd.Series(loaded_model.predict(X))

    # Write prediction
    X.to_csv(args.predict_output, index=False)


if __name__ == "__main__":
    main()
