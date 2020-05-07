#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from masked_face.infrastructure.loader_raw import Loader
from masked_face.infrastructure.command_line_parser import TrainCommandLineParser
from masked_face.domain.data_preparation import ImagePreparation, LabelClassifier
from masked_face.domain.training_optimisation import TrainBySteps


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    """Launch the main process of algorithm training"""
    # Command line parser
    parser = TrainCommandLineParser()
    args = parser.parse_args()

    # Loading images and labels
    logging.info(' Loading images and labels ...')
    loader = Loader(args['data_input'])
    raw_images, raw_labels = loader.get_raw_input()
    logging.info(' Loading done')

    # Images preprocessing
    logging.info(' Starting Preprocessing  ...')
    preprocessing = ImagePreparation(
        raw_images, args['model_type'], args['devmode']
    )
    images = preprocessing.apply_basic_processing()
    logging.info(' Preprocessing done')

    # Labels Encoding
    logging.info(' Starting Labels Encoding ...')
    encoder = LabelClassifier(raw_labels)
    labels, label_classes = encoder.get_categorical_labels()
    logging.info(' Labels Encoding done')

    # Training to optimise the classifier
    logging.info(' Starting Pipeline training ...')
    if args['step_training']:
        TrainBySteps(images, labels, args)
    logging.info(' Model trained and saved ...')


if __name__ == "__main__":
    main()
