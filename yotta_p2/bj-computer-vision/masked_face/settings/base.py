#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

# Path variables
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
RAW_DIR = os.path.join(REPO_DIR, 'data', 'raw')
LOGS_DIR = os.path.join(REPO_DIR, 'logs')
MODELS_DIR = os.path.join(REPO_DIR, 'models')

# Image constants
IMAGE_SIZE = {'MobileNetV2': (224, 224, 3)}

# Model constants
MODEL_CHOICE = 'MobileNetV2'
CLASS_NBR = 2
BATCH_SIZE = 32
INIT_LEARNING_RATE = 1e-4
EPOCHS = 20
MODEL_FILE = os.path.join(MODELS_DIR, MODEL_CHOICE + '-masked_detection.hdf5')
LABELS_NAME = ['masked', 'no_masked']

# Developper mode
DATA_FILE = '/home/latitude/Documents/Yotta/2-Data_Science/Projet_2-CV_NLP/data/final_data'  # TODO removed at the end of development
