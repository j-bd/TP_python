#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to produce interpretability of the model.

For explainer, several options are offered. Keep in mind that some of them
takes lots of times and lots of memory ressource. Thus, we put in comments
many of them.

Classes
-------
Interpretability
"""
import numpy as np
import tensorflow as tf
import shap
from tf_explain.core.activations import ExtractActivations
from tf_explain.core.vanilla_gradients import VanillaGradients
from tf_explain.core.gradients_inputs import GradientsInputs
from tf_explain.core.occlusion_sensitivity import OcclusionSensitivity
from tf_explain.core.grad_cam import GradCAM
from tf_explain.core.smoothgrad import SmoothGrad
from tf_explain.core.integrated_gradients import IntegratedGradients

from masked_face.settings import base
from masked_face.domain.data_preparation import DataPreprocessing


class Interpretability:
    """
    Compute and save tf-explainer and shap interpretability

    Methods
    -------
    tf_explainer_results
    shap_results
    """
    def __init__(self, model, x_set, y_set, args):
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
        args : arguments parser
            user choices
        """
        self.model = model
        self.x_set = x_set
        self.y_set = y_set
        self.args = args
        self.dir = base.INTERPRETABILITY

    def tf_explainer_results(self):
        """Save in 'logs' directory results of TF EXPLAINER interpretability
        under png format.
        Only 4 images of the dataset are selected to avoid CPU overload

        We freezed certains explainers. Indeed, it takes lots of ressources.
        Feel free to unfreeze the one you want.
        """
        preprocess = DataPreprocessing(
            self.x_set[2:4], self.y_set[2:4], self.args
        )
        self.x_val, self.y_val, self.label = preprocess.apply_preprocessing()

        # ExtractActivations
#        explainer = ExtractActivations()
#        if self.args['model_type'] == 'MobileNetV2':
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model, layer_name="Conv_1"
#            )
#        elif self.args['model_type'] == 'VGG16':
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model,
#                layer_name="block5_conv3"
#            )
#        elif self.args['model_type'] == 'Xception':
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model,
#                layer_name="block14_sepconv2_act"
#            )
#        explainer.save(grid, self.dir, "activations.png")

        # VanillaGradients
#        class_index = [0, 1]
#        for idx in class_index:
#            explainer = VanillaGradients()
#            # Compute VanillaGradients on VGG16
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model, idx)
#            explainer.save(grid, self.dir, str(idx) + "vanilla_gradients.png")
#
        # GradientsInputs
#        class_index = [0, 1]
#        for idx in class_index:
#            explainer = GradientsInputs()
#            # Compute GradientsInputs on VGG16
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model, idx)
#            explainer.save(grid, self.dir, str(idx) + "gradients_inputs.png")

        # OcclusionSensitivity
        class_index = [0, 1]
        for idx in class_index:
            explainer = OcclusionSensitivity()
            # Compute Occlusion Sensitivity for patch_size 20
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx, 20)
            explainer.save(
                grid, self.dir, str(idx) + "occlusion_sensitivity_20.png"
            )
            # Compute Occlusion Sensitivity for patch_size 10
            grid = explainer.explain(
                (self.x_val, self.y_val), self.model, idx, 10)
            explainer.save(
                grid, self.dir, str(idx) + "occlusion_sensitivity_10.png"
            )

        # GradCAM
        class_index = [0, 1]
        for idx in class_index:
            explainer = GradCAM()
            if self.args['model_type'] == 'MobileNetV2':
                grid = explainer.explain(
                    (self.x_val, self.y_val), self.model, class_index=idx,
                    layer_name="Conv_1"
                )
            elif self.args['model_type'] == 'VGG16':
                grid = explainer.explain(
                    (self.x_val, self.y_val), self.model, class_index=idx,
                    layer_name="block5_conv3"
                )
            elif self.args['model_type'] == 'Xception':
                grid = explainer.explain(
                    (self.x_val, self.y_val), self.model, class_index=idx,
                    layer_name="block14_sepconv2_act"
                )
            explainer.save(grid, self.dir, str(idx) + "grad_cam.png")

        # SmoothGrad
#        class_index = [0, 1]
#        for idx in class_index:
#            explainer = SmoothGrad()
#            # Compute SmoothGrad on VGG16
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model, idx, 20, 1.0)
#            explainer.save(grid, self.dir, str(idx) + "smoothgrad.png")
#
        # IntegratedGradients
#        class_index = [0, 1]
#        for idx in class_index:
#            explainer = IntegratedGradients()
#            # Compute SmoothGrad on VGG16
#            grid = explainer.explain(
#                (self.x_val, self.y_val), self.model, idx, n_steps=15)
#            explainer.save(grid, self.dir, str(idx) + "integrated_grad.png")

    def shap_results(self):
        """Display results of SHAP interpretability

        Only 4 images of the dataset are selected to avoid CPU overload
        """
        def get_submodel_from(layer, model):
            """Reproduce sequential vgg16"""
            inputs = tf.keras.Input(model.layers[layer].input.shape[1:])
            outputs = inputs
            n_layers = len(model.layers)
            for l in range(layer, n_layers):
                outputs = model.layers[l](outputs)
            submodel = tf.keras.models.Model(inputs=inputs, outputs=outputs)
            return submodel

        def map2layer(x, layer, model, preprocess=True):
            subinputs = tf.keras.models.Model(
                inputs=model.layers[0].input, outputs=model.layers[layer].input
            )
            return subinputs(x).numpy()

        preprocess = DataPreprocessing(
            self.x_set[2:4], self.y_set[2:4], self.args
        )
        self.x_val, self.y_val, self.label = preprocess.apply_preprocessing()

        # Layer choosen to be analysed
        layer = 5  # TODO We could boucle over different layer
        submodel = get_submodel_from(layer=layer, model=self.model)

        # The reference is a black background preprocessed
        reference = map2layer(
            x=np.zeros((1,) + self.x_val.shape[1:]), layer=layer,
            model=self.model, preprocess=True
        )

        explainer = shap.DeepExplainer(submodel, reference)

        subimages = map2layer(
            x=self.x_val, layer=layer, model=self.model, preprocess=True
        )
        shap_values, indices = explainer.shap_values(
            subimages, ranked_outputs=1, check_additivity=False
        )
        shap.image_plot([shap_values[0][[0]]], self.x_val[[0]])
        shap.image_plot([shap_values[0][[1]]], self.x_val[[1]])
