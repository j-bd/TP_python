#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to train models.

Example
-------
Script could be run with the following command line

    $ python masked_face/application/train.py --data_input 'path/to/dir'
    --step_training True --model_type 'MobileNetV2'

--data_input: the directory must contains two directory gathering images. One
called 'masked_face' and the other one 'nude_face'. By default, the master
directory is 'raw' in 'data'.

--step_training: offer the possibility to train with train, validation and test
dataset. If set to 'False', training will be done on the full dataset

--model_type: 3 types of models are offered 'MobileNetV2', 'VGG16', 'Xception'.
If you want to add an other keras model, please add the new model entry images
size in the constant 'IMAGE_SIZE' located in 'masked_face/settings/base.py'
"""
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

        # Model intepretability
        interpreter = Interpretability(model, test_x, test_y, args)
        interpreter.tf_explainer_results()
        if args['model_type'] == 'VGG16':
            interpreter.shap_results()

    else:
        logging.info(' Launching training on full dataset ...')
        model_steps = FullRun(raw_images, raw_labels, args)
        model, history = model_steps.launching_steps()

    logging.info(f' Model trained and saved in {base.MODELS_DIR}')


if __name__ == "__main__":
    main()
