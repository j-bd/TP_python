#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to retrieve models.

Classes
-------
GetModels
"""
import cv2
from tensorflow.keras.models import load_model

from masked_face.settings import base


class GetModels:
    """Set up models.

    Methods
    -------
    models_loading
    """
    def __init__(self, classifier_type: str):
        """Class initialisation

        Parameters
        ----------
        classifier_type : str
            user specification
        """
        self.classifier_type = classifier_type

    def models_loading(self):
        """
        Provide the detector model and the classifier model ready to use

        Returns
        -------
        detector
            caffe model
        classifier
            Keras model user choice
        """
        model_detection_structure = base.MODEL_DETECTION_STRUCTURE
        model_detection_weights = base.MODEL_DETECTION_WEIGHT
        detector = cv2.dnn.readNet(
            model_detection_structure, model_detection_weights
        )
        if self.classifier_type == 'MobileNetV2':
            model_classification = base.MOBNETV2_CLASSIFIER
            classifier = load_model(model_classification)

        elif self.classifier_type == 'VGG16':
            model_classification = base.VGG16_CLASSIFIER
            classifier = load_model(model_classification)

#        elif self.classifier_type == 'Xception':
#            model_classification = base.IMAGE_MODEL_CLASSIFIER_FILE
#            classifier = load_model(model_classification)

        return detector, classifier
