#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to .

Classes
-------

"""
import logging

from masked_face.domain.pipeline_detection import Pipeline
from masked_face.infrastructure.predict_models_loading import GetModels
from masked_face.infrastructure.command_line_parser import PredictCommandLineParser


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    """Launch the main process of predict training"""
    # Command line parser
    parser = PredictCommandLineParser()
    args = parser.parse_args()

    # Detection type choice
    if args['type_detection'] == 'webcam':
        logging.info(' Loading models ...')
        models = GetModels(args['type_detection'])
        detector, classifier = models.models_loading()

        logging.info(' Starting webcam analyse ...')
        logging.info(' To stop processing please press the letter "q"')
        webcam_pipe = Pipeline(detector, classifier, args)
        webcam_pipe.webcam_detection()

    elif args['type_detection'] == 'video':
        logging.info(' Loading models ...')
        models = GetModels(args['type_detection'])
        detector, classifier = models.models_loading()

        logging.info(' Starting video analyse ...')
        logging.info(' To stop processing please press the letter "q"')
        video_pipe = Pipeline(detector, classifier, args)
        video_pipe.video_detection()

    elif args['type_detection'] == 'image':
        logging.info(' Loading models ...')
        models = GetModels(args['type_detection'])
        detector, classifier = models.models_loading()

        logging.info(' Starting video analyse ...')
        logging.info(' To stop processing please press the letter "q"')
        image_pipe = Pipeline(detector, classifier, args)
        image_pipe.image_detection()

    logging.info(' Detection ended')


if __name__ == "__main__":
    main()
