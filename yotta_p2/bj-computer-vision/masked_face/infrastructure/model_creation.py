#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint

from masked_face.settings import base


class ModelConstructor:
    """
    Create model following user choice

    Attributes
    ----------
    model : str
        model selected

    Methods
    -------
    get_model
    _top_layers_constructor
    _base_model
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

        return final_model

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

        # Loop over all layers in the base model and freeze them so they will
        # not be updated during training process
        for layer in base_model.layers:
            layer.trainable = False

        return base_model


class CallbacksConstructor:
    """
    Create Callbacks to improve the following of training

    Attributes
    ----------
    logs_directory : str
        directory where callbacks will be saved
    calbacks : list
        List of callbacks used

    Methods
    -------
    get_callbacks
    _tensor_board
    _checkpoint_call
    """
    def __init__(self, logs_directory):
        """Class initialisation
        Parameters
        ----------
        logs_directory : str
            directory where callbacks will be saved
        """
        self.logs_directory = logs_directory
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
        Will display in an web API the evolution of loss and accuracy

        Returns
        -------
        tensor_board : TensorFlow Object
        """
        tensor_board = TensorBoard(
            log_dir=self.logs_directory, histogram_freq=1, write_graph=True,
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
        fname = os.path.sep.join([self.logs_directory, "weights.hdf5"])
        checkpoint = ModelCheckpoint(
            fname, monitor="val_loss", mode="min", save_best_only=True,
            verbose=1
        )
        return checkpoint
