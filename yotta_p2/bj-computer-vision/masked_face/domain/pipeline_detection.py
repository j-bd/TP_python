#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to organize detection processing.

Classes
-------
Pipeline
"""
import cv2

from masked_face.domain.frame_detection import FrameDetection


class Pipeline:
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
        self.face_detection = model_detector
        self.face_classifier = model_classifier
        self.args = args

    def webcam_detection(self):
        """Retrieve webcam input and analyse each frame
        """
        detection = FrameDetection(
            self.face_detection, self.face_classifier, self.args
        )
        video_capture = cv2.VideoCapture(0)
        while True:
            # Read webcam capture
            ret, frame = video_capture.read()

            detection.launch_detection(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def video_detection(self):
        """Retrieve video input and analyse each frame
        """
        detection = FrameDetection(
            self.face_detection, self.face_classifier, self.args
        )
        video_capture = cv2.VideoCapture(self.args["path_video"])
        while True:
            # Read video capture
            ret, frame = video_capture.read()
            if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
                break

            detection.launch_detection(frame)

        video_capture.release()
        cv2.destroyAllWindows()

    def image_detection(self):
        """Retrieve image input and analyse it
        """
        detection = FrameDetection(
            self.face_detection, self.face_classifier, self.args
        )

        frame = cv2.imread(self.args['path_image'])

        detection.launch_detection(frame)

        cv2.waitKey() & 0xFF == ord('q')
        cv2.destroyAllWindows()
