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
from masked_face.settings import base


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def main():
    """Launch the main process of algorithm training"""
    # Command line parser
    parser = PredictCommandLineParser()
    args = parser.parse_args()

    # Detection type choice
    if args['type_detection'] == 'webcam':
        detection = WebcamDetection(args)
        detection.launch_detection()


if __name__ == "__main__":
    main()
