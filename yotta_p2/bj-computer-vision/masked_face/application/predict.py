#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to make predictions.

Example
-------
Script could be run with the following command line

    $ python masked_face/application/predict.py --type_detection 'video'
    --path_video 'path/to/video.mp4' --classifier_type 'MobileNetV2'

    $ python masked_face/application/predict.py --type_detection 'image'
    --path_image 'path/to/image.jpg' --classifier_type 'MobileNetV2'

--type_detection: 3 types of detection are offered 'image', 'video', 'webcam'.

--path_video: full path to your video

--classifier_type: 3 types of classifiers are offered 'MobileNetV2', 'VGG16',
'Xception'.
"""
import logging

from masked_face.domain.predict_medium import MediumSelection
from masked_face.infrastructure.predict_models_loading import GetModels
from masked_face.infrastructure.command_line_parser import PredictParser


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main(args):
    """Launch the main process of predict training"""
    # Loading models
    logging.info(' Loading models ...')
    models = GetModels(args['classifier_type'])
    detector, classifier = models.models_loading()

    # Launching detection
    processing_medium = MediumSelection(detector, classifier, args)
    processing_medium.medium_pipeline_selection()

    logging.info(' Detection ended')


if __name__ == "__main__":
    # Command line parser
    parser = PredictParser()
    args = parser.parse_args()
    main(args)
