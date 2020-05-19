#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# Path variables
# --------------
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
RAW_DIR = os.path.join(REPO_DIR, 'data', 'raw')
LOGS_DIR = os.path.join(REPO_DIR, 'logs')
MODELS_DIR = os.path.join(REPO_DIR, 'models')
OUTPUT_DIR = os.path.join(REPO_DIR, 'data', 'processed')
PREDICT_DIR = os.path.join(REPO_DIR, 'data', 'external')
IMAGE_GENERATOR = os.path.join(LOGS_DIR, 'image_data_generator')
INTERPRETABILITY = os.path.join(LOGS_DIR, 'interpretability')


# Train variables
# ---------------
# Image constants
IMAGE_SIZE = {
    'MobileNetV2': (224, 224, 3), 'VGG16': (224, 224, 3),
    'Xception': (299, 299, 3)
}

# Classifier Model constants
CLASS_NBR = 2
BATCH_SIZE = 32
INIT_LEARNING_RATE = 1e-2
EPOCHS = 20
LABELS_NAME = ['Masked', 'No_masked']


# Predict variables
# -----------------
MODEL_DETECTION_STRUCTURE = os.path.join(
    MODELS_DIR, 'detector', 'deploy.prototxt'
)
MODEL_DETECTION_WEIGHT = os.path.join(
    MODELS_DIR, 'detector', 'res10_300x300_ssd_iter_140000.caffemodel'
)
MOBNETV2_CLASSIFIER = os.path.join(
    MODELS_DIR, 'classifier', 'MobileNetV2-masked_detection.hdf5'
)
VGG16_CLASSIFIER = os.path.join(
    MODELS_DIR, 'classifier', 'VGG16-masked_detection.hdf5'
)
XCEPTION_CLASSIFIER = os.path.join(
    MODELS_DIR, 'classifier', 'Xception-masked_detection.hdf5'
)
