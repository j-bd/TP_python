#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# Path variables
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
RAW_DIR = os.path.join(REPO_DIR, 'data', 'raw')
LOGS_DIR = os.path.join(REPO_DIR, 'logs')
MODELS_DIR = os.path.join(REPO_DIR, 'models')
OUTPUT_DIR = os.path.join(REPO_DIR, 'data', 'processed')
WEBCAM_DETECTION_DIR = os.path.join(MODELS_DIR, 'webc_face_detector')

# Image constants
IMAGE_SIZE = {'MobileNetV2': (224, 224, 3)}

# Classifier Model constants
MODEL_CHOICE = 'MobileNetV2'
CLASS_NBR = 2
BATCH_SIZE = 32
INIT_LEARNING_RATE = 1e-2
EPOCHS = 20
MODEL_FILE = os.path.join(MODELS_DIR, MODEL_CHOICE + '-masked_detection.hdf5')
LABELS_NAME = ['masked', 'no_masked']

# Webcam Face detector
WEBC_MODEL_DETECTION_STRUCTURE = os.path.join(WEBCAM_DETECTION_DIR, 'deploy.prototxt')
WEBC_MODEL_DETECTION_WEIGHT = os.path.join(WEBCAM_DETECTION_DIR, 'res10_300x300_ssd_iter_140000.caffemodel')

# Developper mode
DATA_FILE = '/home/latitude/Documents/Yotta/2-Data_Science/Projet_2-CV_NLP/data/final_data'  # TODO removed at the end of development
