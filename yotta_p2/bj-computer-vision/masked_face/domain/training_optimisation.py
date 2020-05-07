#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np

from masked_face.settings import base
from masked_face.infrastructure import model_creation
#from masked_face.domain.data_generator import DataGenerator


from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report


class TrainBySteps:

    def __init__(self, images_id: list, labels: dict, args):
        self.images_id = images_id
        self.labels = labels
        self.directory = args['model_output']
        self.model_type = args['model_type']
        self.train()

#    def train(self):
#        generator = DataGenerator(self.images_id, self.labels,
#            batch_size=base.BATCH_SIZE, dim=base.IMAGE_SIZE['MobileNetV2'],
#            n_classes=base.CLASS_NBR, shuffle=True, self.directory)

    def train(self):
        train_x, test_x, train_y, test_y = self._data_split()

        model_creator = model_creation.ModelConstructor(self.model_type)
        model = model_creator.get_model()

        # Callbacks creation
        checkpoint_save = self.checkpoint_call(self.directory)
        tensor_board = TensorBoard(
            log_dir=self.directory, histogram_freq=1, write_graph=True,
            write_images=True
        )
        callbacks = [checkpoint_save, tensor_board]

        # compile our model
        print("[INFO] compiling model...")
        opt = Adam(
                lr=base.INIT_LEARNING_RATE,
                decay=base.INIT_LEARNING_RATE / base.EPOCHS)
        model.compile(loss="binary_crossentropy", optimizer=opt,
                      metrics=["accuracy"])
        # train the head of the network
#        train_x = np.expand_dims(train_x, axis=0)
#        train_x = tf.expand_dims(train_x, 0)

        augmentation = ImageDataGenerator(
                rotation_range=15,
                fill_mode="nearest")


        print("[INFO] training head...")
        history = model.fit(
            augmentation.flow(train_x, train_y, batch_size=base.BATCH_SIZE),
            epochs=base.EPOCHS, validation_data=(test_x, test_y),
            callbacks=callbacks)
#        steps_per_epoch=len(trainX) // BS,
#	validation_data=(testX, testY),
#	validation_steps=len(testX) // BS,
#	epochs=EPOCHS)


        lab_name = ['masked', 'no_masked']
        self.model_evaluation(model, test_x, test_y, lab_name)

        self.display_learning_evol(history, self.directory)

        return model, history

    def _data_split(self):
        train_x, test_x, train_y, test_y = train_test_split(
            self.images_id, self.labels, test_size=0.20, stratify=self.labels,
            random_state=42
        )
        return train_x, test_x, train_y, test_y

    def checkpoint_call(self, directory):
        '''Return a callback checkpoint configuration to save only the best model'''
        fname = os.path.sep.join([directory, "weights.hdf5"])
        checkpoint = ModelCheckpoint(
            fname, monitor="val_loss", mode="min", save_best_only=True,
            verbose=1
        )
        return checkpoint

    def model_evaluation(self, model, test_x, test_y, label_names):
        '''Display on terminal command the quality of model's predictions'''
        print("[INFO] Evaluating network...")
        predictions = model.predict(test_x, batch_size=64)
        print(
            classification_report(
                test_y.argmax(axis=1), predictions.argmax(axis=1),
                target_names=label_names
            )
        )

    def display_learning_evol(self, history_dic, directory):
        '''Plot the training loss and accuracy'''
        fname = os.path.sep.join([directory, "loss_accuracy_history.png"])
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(
            np.arange(0, len(history_dic.history["loss"])),
            history_dic.history["loss"], label="train_loss"
        )
        plt.plot(
            np.arange(0, len(history_dic.history["val_loss"])),
            history_dic.history["val_loss"], label="val_loss"
        )
        plt.plot(
            np.arange(0, len(history_dic.history["accuracy"])),
            history_dic.history["accuracy"], label="train_acc"
        )
        plt.plot(
            np.arange(0, len(history_dic.history["val_accuracy"])),
            history_dic.history["val_accuracy"], label="val_accuracy"
        )
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend()
        plt.savefig(fname)
