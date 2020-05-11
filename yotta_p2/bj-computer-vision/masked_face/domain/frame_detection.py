#!/usr/bin/env python
# coding: utf-8
"""
Module to realize masked faces detection based on a face detector model and a
classifier model

Classes
-------
FrameDetection
"""
import cv2
import numpy as np
import imutils

from masked_face.settings import base
from masked_face.domain.data_preparation import ImagePreparation


class FrameDetection:
    """
    Use provide frame to detect if a person wear or not a mask

    Methods
    -------
    launch_detection
    _face_detection
    _detections_filter
    _faces_classification
    _display_results
    """
    def __init__(self, detection, classifier, args):
        """Class initialisation

        Parameters
        ----------
        detection
            model
        classifier
            model
        args : ArgumentParser
            user specification
        """
        self.devmode = args['devmode']
        self.confidence = args["confidence"]
        self.face_detector = detection
        self.face_classifier = classifier

    def launch_detection(self, frame):
        """
        Process webcam video through all the pipeline detection
        """
        # Resize frame for detector
        frame = imutils.resize(frame, width=400)

        # Faces Detection
        detections = self._face_detection(frame)

        # Detections filtering
        faces, locations = self._detections_filter(frame, detections)

        # Face classification
        predictions = self._faces_classification(faces)

        # Display results
        self._display_results(frame, predictions, locations)

        cv2.imshow('Video', frame)

    def _face_detection(self, frame):
        """
        Detect if there is or not face on video flow

        Parameters
        ----------
        frame : numpy array
            bgr style

        Returns
        -------
        detections
            result of detection model analyse
        """
        # Image preprocessing
        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), (104.0, 177.0, 123.0)
        )
        # Face Detection
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()
        return detections

    def _detections_filter(self, frame, detections):
        """
        Remove face detection with a weak probability of being a person. User
        gives the threshold with parser argument

        Parameters
        ----------
        frame : numpy array
            bgr style
        detections
            result of detection model analyse

        Returns
        -------
        faces : list
            relevant face selection
        locs : list
            bounding box of selected faces
        """
        faces = []
        locations = []
        (h, w) = frame.shape[:2]

        for idx in range(0, detections.shape[2]):
            # Targets interest detections (greater than user threshold)
            detection_confidence = detections[0, 0, idx, 2]

            if detection_confidence > self.confidence:
                # Retrieve face bounding box
                box = detections[0, 0, idx, 3:7] * np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")
                # Clean extreme value (avoid exceeding image border)
                (start_x, start_y) = (max(0, start_x), max(0, start_y))
                (end_x, end_y) = (min(w - 1, end_x), min(h - 1, end_y))
                # Crop face result and stock it with corresponding bounding box
                face = frame[start_y:end_y, start_x:end_x]
                faces.append(face)
                locations.append((start_x, start_y, end_x, end_y))
        return faces, locations

    def _faces_classification(self, faces):
        """
        Launch analyse to determine if a person is masked or not

        Parameters
        ----------
        frame : numpy array
            bgr style

        Returns
        -------
        predictions : list
            probability of having or not a mask
        """
        predictions = []
        if len(faces) > 0:
            # Preprocess face before pushing in classifier prediction
            preprocessing = ImagePreparation(
                faces, base.WEBC_MODEL_CLASSIFIER, False
            )
            faces = preprocessing.apply_basic_processing()
            predictions = self.face_classifier.predict(faces)
        return predictions

    def _display_results(self, frame, predictions, localisations):
        """
        Display the original frame and add a bounding box with text

        Parameters
        ----------
        frame : numpy array
            bgr style
        predictions : list
            probability of having or not a mask
        localisations : list
            bounding box of selected faces
        """
        if self.devmode:
            print(f"localisations = {localisations}")
            print(f"predictions = {predictions}")
        for (bounding_box, prediction) in zip(localisations, predictions):
            (start_x, start_y, end_x, end_y) = bounding_box
            (mask, without_mask) = prediction
            # Set up colour and message
            if mask > without_mask:
                label = "Mask"
                color = (0, 255, 0)
            else:
                label = "No Mask"
                color = (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, without_mask) * 100)

            cv2.putText(
                frame, label, (start_x, start_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2
            )
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), color, 2)
