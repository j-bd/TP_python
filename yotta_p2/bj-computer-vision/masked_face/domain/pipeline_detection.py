#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import imutils

from masked_face.settings import base
from masked_face.domain.data_preparation import ImagePreparation


class WebcamDetection:

    def __init__(self, args):
        """
        """
        self.devmode = args['devmode']
        self.confidence = args["confidence"]
        self.model_classification = base.MODEL_FILE
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

            # Faces Detection
            detections = self._face_detection(frame)

            # Detections filtering
            faces, locs = self._detections_filter(frame, detections)

            # Face classification
            predictions = self._faces_classification(faces)

            # Display results
            self._display_results(frame, predictions, locs)

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

    def _faces_classification(self, faces):
        """
        """
        predictions = []
        preprocessing = ImagePreparation(
                faces, base.WEBC_MODEL_CLASSIFIER, self.devmode
        )
        faces = preprocessing.apply_basic_processing()
        if len(faces) > 0:
            # for faster inference we'll make batch predictions on *all*
            # faces at the same time rather than one-by-one predictions
            # in the above `for` loop
            predictions = self.face_classifier.predict(faces)
        return predictions

    def _display_results(self, frame, predictions, localisation):
        """
        """
        print(localisation)
        print(predictions)
        for (box, pred) in zip(localisation, predictions):
            # unpack the bounding box and predictions
            (start_x, start_y, end_x, end_y) = box
            (mask, withoutMask) = pred
            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (start_x, start_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), color, 2)
