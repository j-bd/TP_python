#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to organize detection processing.

Classes
-------
MediumSelection
"""
import logging

import cv2
import streamlit as st

from masked_face.domain.frame_detection import FrameDetection


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class MediumSelection:
    """Detection processing.

    Methods
    -------
    webcam_detection
    video_detection
    image_detection
    """
    def __init__(self, model_detector, model_classifier, args):
        """Class initialisation

        Parameters
        ----------
        model_detector
        model_classifier
        args : ArgumentsParser
        """
        self.detection = FrameDetection(model_detector, model_classifier, args)
        self.streamlit_window = st.empty()
        self.args = args

    def medium_pipeline_selection(self):
        """Launch pipeline corresponding to image, video or webcam
        """
        logging.info(' To stop processing please press the letter "q"')

        if self.args['type_detection'] == 'webcam':
            logging.info(' Starting webcam analyse ...')
            self._webcam_detection()
        elif self.args['type_detection'] == 'video':
            logging.info(' Starting video analyse ...')
            self._video_detection()
        elif self.args['type_detection'] == 'image':
            logging.info(' Starting image analyse ...')
            self._image_detection()

    def _webcam_detection(self):
        """Retrieve webcam input and analyse each frame
        """
        video_capture = cv2.VideoCapture(0)

        while True:
            # Read webcam capture
            ret, frame = video_capture.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.detection.launch_detection(frame, self.streamlit_window)

        video_capture.release()
        cv2.destroyAllWindows()

    def _video_detection(self):
        """Retrieve video input and analyse each frame
        """
        video_capture = cv2.VideoCapture(self.args["path_video"])

        while True:
            # Read video capture
            ret, frame = video_capture.read()
            if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.detection.launch_detection(frame, self.streamlit_window)

        video_capture.release()
        cv2.destroyAllWindows()

    def _image_detection(self):
        """Retrieve image input and analyse it
        """
        frame = cv2.imread(self.args['path_image'])

        self.detection.launch_detection(frame, self.streamlit_window)

        cv2.waitKey() & 0xFF == ord('q')
        cv2.destroyAllWindows()
