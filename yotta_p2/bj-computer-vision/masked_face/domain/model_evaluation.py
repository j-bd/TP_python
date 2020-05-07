#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 14:55:30 2020

@author: j-bd
"""
import os
import logging

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report

from masked_face.settings import base


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class ModelResultEvaluation:

    def __init__(self, model, test_x, test_y, history: dict, directory: str):
        self.model = model
        self.test_x = test_x
        self.test_y = test_y
        self.history = history
        self.directory = directory

    def get_evaluation(self):
        self._model_evaluation()
        self._display_learning_evol()
        logging.info(f' Plot available in {self.directory}')

    def _model_evaluation(self):
        '''Display on terminal command the quality of model's predictions'''
        predictions = self.model.predict(self.test_x, batch_size=64)
        print(
            classification_report(
                self.test_y.argmax(axis=1), predictions.argmax(axis=1),
                target_names=base.LABELS_NAME
            )
        )

    def _display_learning_evol(self):
        '''Plot the training loss and accuracy'''
        fname = os.path.sep.join([self.directory, "loss_accuracy_history.png"])
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(
            np.arange(0, len(self.history.history["loss"])),
            self.history.history["loss"], label="train_loss"
        )
        plt.plot(
            np.arange(0, len(self.history.history["val_loss"])),
            self.history.history["val_loss"], label="val_loss"
        )
        plt.plot(
            np.arange(0, len(self.history.history["accuracy"])),
            self.history.history["accuracy"], label="train_acc"
        )
        plt.plot(
            np.arange(0, len(self.history.history["val_accuracy"])),
            self.history.history["val_accuracy"], label="val_accuracy"
        )
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend()
        plt.savefig(fname)
