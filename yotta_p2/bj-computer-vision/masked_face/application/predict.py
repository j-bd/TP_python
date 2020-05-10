#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to .

Classes
-------

"""
import logging

from masked_face.domain.pipeline_detection import WebcamDetection
from masked_face.infrastructure.command_line_parser import PredictCommandLineParser


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    """Launch the main process of algorithm training"""
    # Command line parser
    parser = PredictCommandLineParser()
    args = parser.parse_args()

    # Detection type choice
    if args['type_detection'] == 'webcam':
        detection = WebcamDetection(args)
        logging.info(' Starting webcam analyse ...')
        logging.info(' To stop processing please press the letter "q"')
        detection.launch_detection()
        logging.info(' Detection ended')


if __name__ == "__main__":
    main()
