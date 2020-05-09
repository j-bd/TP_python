#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import cv2
import numpy as np
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
            # Read webcam capture
            ret, frame = video_capture.read()

            # Resize frame for detector
            frame = imutils.resize(frame, width=400)

            # Face Detection
            detections = self._face_detection(frame)

            # Detection filtering
            faces, locs = self._detections_filter(frame, detections)

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
        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), (104.0, 177.0, 123.0)
        )
        # pass the blob through the network and obtain the face detections
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()
        return detections

    def _detections_filter(self, frame, detections):
        """
        """
        faces = []
        locs = []
        (h, w) = frame.shape[:2]
        # loop over the detections
        for idx in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the detection
            detection_confidence = detections[0, 0, idx, 2]
            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if detection_confidence > self.confidence:
                # compute the (x, y)-coordinates of the bounding box for
                # the object
                box = detections[0, 0, idx, 3:7] * np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")
                # ensure the bounding boxes fall within the dimensions of
                # the frame
                (start_x, start_y) = (max(0, start_x), max(0, start_y))
                (end_x, end_y) = (min(w - 1, end_x), min(h - 1, end_y))

                # extract the face ROI, convert it from BGR to RGB channel
                # ordering, resize it to 224x224, and preprocess it
                face = frame[start_y:end_y, start_x:end_x]
#                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#                face = cv2.resize(face, (224, 224))
#                face = img_to_array(face)
#                face = preprocess_input(face)
#                face = np.expand_dims(face, axis=0)
                # add the face and bounding boxes to their respective
                # lists
                faces.append(face)
                locs.append((start_x, start_y, end_x, end_y))
        return faces, locs
