#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to analyse model performance.

Classes
-------
ModelResultEvaluation
"""
import os
import logging

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report

from masked_face.settings import base


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class ModelResultEvaluation:
    """
    Compute and display model evaluation (loss, accuracy and classification
    report)

    Methods
    -------
    get_evaluation
    _model_evaluation
    _display_learning_evol
    """
    def __init__(self, model, test_x, test_y, history: dict):
        """Class initialisation

        Parameters
        ----------
        model : TensorFlow Keras model
            model trained
        test_x, test_y : test data (images and label)
        history : dict
            history of every training epochs
        directory : str
            path to directory where to save outputs
        """
        self.model = model
        self.test_x = test_x
        self.test_y = test_y
        self.history = history

    def get_evaluation(self):
        """
        Launch the mains steps of the evaluation
        """
        self._model_evaluation()
        self._display_learning_evol()
        logging.info(f' Plot available in {base.LOGS_DIR}')

    def _model_evaluation(self):
        """
        Display on terminal command the quality of model's predictions

        Returns
        -------
        Print into consol the classification report
        """
        predictions = self.model.predict(self.test_x, batch_size=64)
        print(
            classification_report(
                self.test_y.argmax(axis=1), predictions.argmax(axis=1),
                target_names=base.LABELS_NAME
            )
        )

    def _display_learning_evol(self):
        """
        Plot the training loss and accuracy

        Returns
        -------
        Save the graph into logs directory
        """
        fname = os.path.join(base.LOGS_DIR, "loss_accuracy_history.png")
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
        plt.title("Evolution of Loss and Accuracy during training")
        plt.xlabel("Epoch Numbers")
        plt.ylabel("Loss/Accuracy Training values")
        plt.legend()
        plt.savefig(fname)
