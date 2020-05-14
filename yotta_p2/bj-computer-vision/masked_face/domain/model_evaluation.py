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

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

from masked_face.settings import base
from masked_face.domain.data_preparation import DataPreprocessing


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
    def __init__(self, model, test_x, test_y, history: dict, args):
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
        self.args = args

    def get_evaluation(self):
        """
        Launch the mains steps of the evaluation
        """
        preprocess = DataPreprocessing(self.test_x, self.test_y, self.args)
        self.test_x, self.test_y, self.label_cl = preprocess.apply_preprocessing()

        self._model_evaluation()
        self._display_learning_evol()
        logging.info(f' Plots available in {base.LOGS_DIR}')

    def _model_evaluation(self):
        """
        Display on terminal command the quality of model's predictions

        Returns
        -------
        Print into consol the classification report
        """
        predictions = self.model.predict(self.test_x, batch_size=64)

        # Classification report display in terminal
        print(
            classification_report(
                self.test_y.argmax(axis=1), predictions.argmax(axis=1),
                target_names=self.label_cl  # base.LABELS_NAME
            )
        )

        # Confusion matrix saved into log directory and display in terminal
        fname = os.path.join(base.LOGS_DIR, "confusion matrix.png")
        c_m = confusion_matrix(
            self.test_y.argmax(axis=1), predictions.argmax(axis=1)
        )
        logging.info(' Confusion Matrix')
        print(c_m)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(c_m)
        plt.title('Confusion matrix of the classifier')
        fig.colorbar(cax)
        ax.set_xticklabels([''] + base.LABELS_NAME)
        ax.set_yticklabels([''] + base.LABELS_NAME)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        for (i, j), z in np.ndenumerate(c_m):
            ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
        plt.savefig(fname)

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
