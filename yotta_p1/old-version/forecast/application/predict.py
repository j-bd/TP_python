#!/usr/bin/env python
# coding: utf-8

import joblib

from forecast.infrastructure.command_line_parser import PredictCommandLineParser
from forecast.infrastructure.preprocessing import Preprocessing


def main():

    # Command line parser
    parser = PredictCommandLineParser()
    args = parser.parse_args()

    # Preprocessing of raw data
    preprocessing = Preprocessing(args.data_input, args.socio_eco_input, args.merge_output)

    # Get features
    X = preprocessing.get_features()

    # Load the model from disk
    loaded_model = joblib.load(args.model_input)

    # Predict target
    y = loaded_model.predict(X)

    # Should write predicted DataFrame somewhere
    import pandas as pd
    X["PREDICTION"] = pd.Series(y)


if __name__ == "__main__":
    main()
