#!/usr/bin/env python
# coding: utf-8
"""
Module to realize masked faces detection based on a face detector model and a
classifier model

Classes
-------
WebcamDetection
"""
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import imutils

from masked_face.settings import base
from masked_face.domain.data_preparation import ImagePreparation


class WebcamDetection:
    """
    Use user Webcam computer to detect if a person wear or not a mask

    Methods
    -------
    launch_detection
    _models_loading
    _face_detection
    _detections_filter
    _faces_classification
    _display_results
    """
    def __init__(self, args):
        """Class initialisation
        Parameters
        ----------
        args : ArgumentParser.
            user specification
        """
        self.devmode = args['devmode']
        self.confidence = args["confidence"]
        self.model_classification = base.MODEL_FILE
        self.model_detection_structure = base.WEBC_MODEL_DETECTION_STRUCTURE
        self.model_detection_weights = base.WEBC_MODEL_DETECTION_WEIGHT
        self.face_detector, self.face_classifier = self._models_loading()

    def launch_detection(self):
        """
        Process webcam video through all the pipeline detection
        """
        video_capture = cv2.VideoCapture(0)
        while True:
            # Read webcam capture
            ret, frame = video_capture.read()

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
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def _models_loading(self):
        """
        Provide the detector model and the classifier model ready to use

        Returns
        -------
        detector
            caffe model
        classifier
            MobileNetv2 Keras model
        """
        detector = cv2.dnn.readNet(
            self.model_detection_structure, self.model_detection_weights
        )
        classifier = load_model(self.model_classification)
        return detector, classifier

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
