#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to create model structure and an other model to monitor training

Classes
-------
ModelConstructor
CallbacksConstructor
"""
import os

from tensorflow.keras.applications import MobileNetV2, VGG16, Xception
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam

from masked_face.settings import base


class ModelConstructor:
    """
    Create model following user choice

    Methods
    -------
    get_model
    _top_layers_constructor
    _base_model
    _optimizer
    """
    def __init__(self, model: str):
        """Class initialisation

        Parameters
        ----------
        model : str
            model selected by user
        """
        self.model = model

    def get_model(self):
        """
        Return the constructed model: base + featured top layers

        Returns
        -------
        final_model : TensorFlow Keras model
            Keras pretrained model + tunned top layers
        """
        base_model = self._base_model()
        head_model = self._top_layers_constructor(base_model)
        final_model = Model(inputs=base_model.input, outputs=head_model)

        model = self._optimizer(final_model)

        model.summary()
        return model

    def _top_layers_constructor(self, base_model):
        """
        Construct the head of the model that will be placed on top of the
        base model

        Parameters
        ----------
        base_model : Keras pre-existing model

        Returns
        -------
        head_model : Keras layers
            Tunned top layer
        """
        head_model = base_model.output
        head_model = AveragePooling2D(pool_size=(7, 7))(head_model)
        head_model = Flatten(name="flatten")(head_model)
        head_model = Dense(128, activation="relu")(head_model)
        head_model = Dropout(0.5)(head_model)
        head_model = Dense(2, activation="softmax")(head_model)
        return head_model

    def _base_model(self):
        """
        Download user choosen pretrained model and realise set up

        Returns
        -------
        base_model : Keras model
            Keras pretrained model + with frozen layers
        """
        if self.model == 'MobileNetV2':
            base_model = MobileNetV2(
                weights="imagenet", include_top=False,
                input_tensor=Input(shape=base.IMAGE_SIZE[self.model])
            )
        elif self.model == 'VGG16':
            base_model = VGG16(
                weights="imagenet", include_top=False,
                input_tensor=Input(shape=base.IMAGE_SIZE[self.model])
            )
        elif self.model == 'Xception':
            base_model = Xception(
                weights="imagenet", include_top=False,
                input_tensor=Input(shape=base.IMAGE_SIZE[self.model])
            )

        # Loop over all layers in the base model and freeze them so they will
        # not be updated during training process
        for layer in base_model.layers:
            layer.trainable = False

        return base_model

    def _optimizer(self, model):
        """Parameters for a stochastic gradient descent method that is based
        on adaptive estimation of first-order and second-order moments : Adam

        Parameters
        ----------
        model : Keras model
            Keras pretrained model

        Returns
        -------
        model : Keras model
            Keras compile model
        """
        opt = Adam(
            lr=base.INIT_LEARNING_RATE,
            decay=base.INIT_LEARNING_RATE / base.EPOCHS
        )
        model.compile(
            loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"]
        )
        return model


class CallbacksConstructor:
    """
    Create Callbacks to improve the following of training

    Methods
    -------
    get_callbacks
    _tensor_board
    _checkpoint_call
    """
    def __init__(self, model: str):
        """
        Class initialisation

        Parameters
        ----------
        model : str
            model selected by user
        """
        self.model = model
        self.calbacks = []

    def get_callbacks(self):
        """
        Return the full callbacks list

        Returns
        -------
        calbacks : list
            list of TensorFlow Objects
        """
        self.calbacks.append(self._checkpoint_call())
        self.calbacks.append(self._tensor_board())
        return self.calbacks

    def _tensor_board(self):
        """
        Will display in an web API the evolution of loss and accuracy. To be
        activate with the following command in the terminal:
        tensorboard --logdir='path/to/tensorboard/folder

        Returns
        -------
        tensor_board : TensorFlow Object
        """
        tensor_board = TensorBoard(
            log_dir=base.LOGS_DIR, histogram_freq=1, write_graph=True,
            write_images=True
        )
        return tensor_board

    def _checkpoint_call(self):
        """
        Return a callback checkpoint configuration to save only the best model
        between each iteration

        Returns
        -------
        checkpoint : TensorFlow Object
        """
        fname = os.path.join(
            base.MODELS_DIR, self.model + '-masked_detection.hdf5')
        checkpoint = ModelCheckpoint(
            fname, monitor="val_loss", mode="min", save_best_only=True,
            verbose=1
        )
        return checkpoint
