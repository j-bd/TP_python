#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging

from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report

from masked_face.settings import base
from masked_face.infrastructure.model_creation import ModelConstructor, CallbacksConstructor
from masked_face.domain.model_evaluation import ModelResultEvaluation
#from masked_face.domain.data_generator import DataGenerator


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class TrainBySteps:

    def __init__(self, images_id: list, labels: dict, args):
        self.images_id = images_id
        self.labels = labels
        self.directory = args['model_output']
        self.model_type = args['model_type']
        self.train()

    def train(self):
        # Splitting Data
        logging.info(' Splitting Data ...')
        train_x, test_x, train_y, test_y = train_test_split(
            self.images_id, self.labels, test_size=0.20, stratify=self.labels,
            random_state=42
        )

        # Neural Network structure creation
        logging.info(' Model infrastructure construction ...')
        model_creator = ModelConstructor(self.model_type)
        model = model_creator.get_model()

        # Callbacks creation
        logging.info(' Callbacks calling ...')
        callbacks_creator = CallbacksConstructor(self.directory)  # TODO args log
        callbacks = callbacks_creator.get_callbacks()

        # Compile the model
        logging.info(' Compiling model ...')
        opt = Adam(
            lr=base.INIT_LEARNING_RATE,
            decay=base.INIT_LEARNING_RATE / base.EPOCHS
        )
        model.compile(
            loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"]
        )
        model.summary()

        augmentation = ImageDataGenerator(
                rotation_range=15,
                fill_mode="nearest")

        # Launch model training
        logging.info(' Training model ...')
        history = model.fit(
            augmentation.flow(train_x, train_y, batch_size=base.BATCH_SIZE),
            epochs=base.EPOCHS, validation_data=(test_x, test_y),
            callbacks=callbacks)
#        steps_per_epoch=len(trainX) // BS,
#	validation_steps=len(testX) // BS,
#	epochs=EPOCHS)

        # Model results analysing steps
        logging.info(' Model Evaluation ...')
        model_evaluation = ModelResultEvaluation(
            model, test_x, test_y, history, self.directory
        )
        model_evaluation.get_evaluation()

        return model, history
