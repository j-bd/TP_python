#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from sklearn.model_selection import train_test_split

from masked_face.infrastructure.loader import Loader
from masked_face.infrastructure.command_line_parser import TrainParser
from masked_face.domain.run_selection import StepsRun, FullRun
from masked_face.domain.model_evaluation import ModelResultEvaluation
from masked_face.domain.model_interpretability import Interpretability
from masked_face.settings import base


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    """Launch the main process of algorithm training"""
    # Command line parser
    parser = TrainParser()
    args = parser.parse_args()

    # Loading images and labels
    logging.info(' Loading images and labels paths ...')
    loader = Loader(args['data_input'])
    raw_images, raw_labels = loader.get_raw_input()
    logging.info(' Loading done')

    # Training to optimise the classifier
    logging.info(' Starting Pipeline training ...')

    if args['step_training']:
        logging.info(' Launching training with validation test ...')
        # Splitting Data in training - test
        logging.info(' Splitting Data ...')
        train_x, test_x, train_y, test_y = train_test_split(
            raw_images, raw_labels, test_size=0.10, stratify=raw_labels,
            random_state=42
        )
        # Model training
        model_steps = StepsRun(train_x, train_y, args)
        model, history = model_steps.launching_steps()

        # Model evaluation
        model_evaluation = ModelResultEvaluation(
            model, test_x, test_y, history, args
        )
        model_evaluation.get_evaluation()
        interpreter = Interpretability(model, test_x, test_y, args)
        interpreter.get_interpretability_results()
#        interpreter.shap_results()

    else:
        logging.info(' Launching training on full dataset ...')
        model_steps = FullRun(raw_images, raw_labels, args)
        model, history = model_steps.launching_steps()

    logging.info(f' Model trained and saved in {base.LOGS_DIR}')


if __name__ == "__main__":
    main()
