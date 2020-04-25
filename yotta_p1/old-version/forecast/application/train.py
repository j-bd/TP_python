#!/usr/bin/env python
# coding: utf-8
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

import joblib
from sklearn.model_selection import train_test_split

from forecast.infrastructure.command_line_parser import TrainCommandLineParser
from forecast.infrastructure.preprocessing import Preprocessing
from forecast.domain import model_train, model_evaluation



def main():
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


    # Command line parser
    parser = TrainCommandLineParser()
    args = parser.parse_args()

    # Preprocessing of raw data
    logging.info('Data cleaning on going ...')
    preprocessing = Preprocessing(args.data_input, args.socio_eco_input, args.merge_output)

    # Get features and target
    X, y = preprocessing.get_features_target()

    # Train test splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    # Training model
    logging.info('Model training on going ...')
    model = model_train.train(X_train, y_train, args.optimisation)
    logging.info('Model trained')

    # Evalutate model
    logging.info('Model evaluation ...')
    default_prediction_rate = 1 - y.sum() / len(y)
    model_evaluation.evaluation(model, X_test, y_test, default_prediction_rate)

    # Export the classifier to a file
    joblib.dump(model, args.model_output)
    logging.info('Model saved')

if __name__ == "__main__":
    main()
