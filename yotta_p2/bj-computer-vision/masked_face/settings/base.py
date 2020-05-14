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
IMAGE_SIZE = {'MobileNetV2': (224, 224, 3)}

# Classifier Model constants
MODEL_CHOICE = 'MobileNetV2'
CLASS_NBR = 2
BATCH_SIZE = 32
INIT_LEARNING_RATE = 1e-2
EPOCHS = 2
MODEL_FILE = os.path.join(MODELS_DIR, MODEL_CHOICE + '-masked_detection.hdf5')
LABELS_NAME = ['masked', 'no_masked']


# Predict variables
# -----------------
# Webcam Face detector
WEBC_MODEL_CLASSIFIER = 'MobileNetV2'
WEBC_MODEL_CLASSIFIER_FILE = os.path.join(
    MODELS_DIR, WEBC_MODEL_CLASSIFIER + '-masked_detection.hdf5'
)
WEBC_MODEL_DETECTION_STRUCTURE = os.path.join(
    MODELS_DIR, 'res10_caffe', 'deploy.prototxt'
)
WEBC_MODEL_DETECTION_WEIGHT = os.path.join(
    MODELS_DIR, 'res10_caffe', 'res10_300x300_ssd_iter_140000.caffemodel'
)

# Video Face detector
VIDEO_MODEL_CLASSIFIER = 'MobileNetV2'
VIDEO_MODEL_CLASSIFIER_FILE = os.path.join(
    MODELS_DIR, VIDEO_MODEL_CLASSIFIER + '-masked_detection.hdf5'
)
VIDEO_MODEL_DETECTION_STRUCTURE = os.path.join(
    MODELS_DIR, 'res10_caffe', 'deploy.prototxt'
)
VIDEO_MODEL_DETECTION_WEIGHT = os.path.join(
    MODELS_DIR, 'res10_caffe', 'res10_300x300_ssd_iter_140000.caffemodel'
)
VIDEO_FILE = os.path.join(PREDICT_DIR, 'video2predict', 'video.mp4')

# Image Face detector
IMAGE_MODEL_CLASSIFIER = 'MobileNetV2'
IMAGE_MODEL_CLASSIFIER_FILE = os.path.join(
    MODELS_DIR, IMAGE_MODEL_CLASSIFIER + '-masked_detection.hdf5'
)
IMAGE_MODEL_DETECTION_STRUCTURE = os.path.join(
    MODELS_DIR, 'res10_caffe', 'deploy.prototxt'
)
IMAGE_MODEL_DETECTION_WEIGHT = os.path.join(
    MODELS_DIR, 'res10_caffe', 'res10_300x300_ssd_iter_140000.caffemodel'
)
IMAGE_FILE = os.path.join(PREDICT_DIR, 'image2predict', 'image.jpeg')


# Developper mode
# ---------------
DATA_FILE = '/home/latitude/Documents/Yotta/2-Data_Science/Projet_2-CV_NLP/data/temp_data'  # TODO removed at the end of development
