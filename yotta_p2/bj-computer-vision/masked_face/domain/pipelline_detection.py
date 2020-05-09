#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import cv2
from tensorflow.keras.models import load_model
import imutils

from masked_face.settings import base


class WebcamDetection:

    def __init__(self, args):
        """
        """
        self.model_detection = args["face_detection"]  # TODO to removed ?
        self.model_classification = args["face_classification"]
        self.confidence = args["confidence"]
        self.model_detection_structure = base.WEBC_MODEL_DETECTION_STRUCTURE
        self.model_detection_weight = base.WEBC_MODEL_DETECTION_WEIGHT
        self.face_detector, self.face_classifier = self._models_loading()

    def launch_detection(self):
        """
        """
        video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = video_capture.read()

            # Resize frame for detector
            frame = imutils.resize(frame, width=400)

            # Face Detection
            detections = self._face_detection(frame)

            # Detection filtering


            # Face classification


            # Display results


            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def _models_loading(self):
        """
        """
        detector = cv2.dnn.readNet(
            self.model_detection_structure, self.model_detection_weight
        )
        classifier = load_model(self.model_classification)
        return detector, classifier

    def _face_detection(self, frame):
        """
        """
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), (104.0, 177.0, 123.0)
        )
        # pass the blob through the network and obtain the face detections
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()
        return detections

    def _detections_filter(self):
        """
        """

